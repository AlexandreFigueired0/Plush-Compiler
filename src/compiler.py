from ast_nodes import *
from type_checker import type_check_program

OPS = {  
    Add: "add",
    Sub: "sub",
    Mul: "mul",
    Div: "sdiv",
    Mod: "srem",
    Equal: "eq",
    NotEqual: "ne",
    LessThan: "slt",
    LessThanOrEqual: "sle",
    GreaterThan: "sgt",
    GreaterThanOrEqual: "sge",
    And: "and",
    Or: "or",
    LogicNot: "not",
    UnaryMinus: "sub",
    Power: "pow",
}

class Emitter(object):
    def __init__(self):
        self.count = 0
        self.lines = []
        # will contain the id of the var in this scope
        self.context = [{}]

        # will cotain the register name for the static strings
        self.strings = {}

    def decl_var(self, name):
        self.context[-1][name] = self.get_count()

    def get_count(self):
        self.count += 1
        return self.count
    
    def is_in_global_context(self):
        return len(self.context) == 1

    def get_temp(self):
        id = self.get_count()
        return f"tmp_{id}"

    def __lshift__(self, v):
        self.lines.append(v)

    def get_code(self):
        return "\n".join(self.lines)

    def get_pointer_name(self, vname):
        for i,ctx in enumerate(reversed(self.context)):
            if vname in ctx:
                ref = "@" if i == (len(self.context)-1) else "%"
                return f"{ref}{vname}{ctx[vname]}"
        raise ValueError(f"Variable {vname} not found in context")
    
    def get_llvm_code_to_store(self,expr, pname, llvm_type):
        compiled_expr = compile(self, expr)
        match expr.type_:
            case StringType():
                # expr is a String
                str_len = len(expr.value) + 1
                return f"\tstore i8* getelementptr inbounds ([{str_len} x i8], [{str_len} x i8]* {compiled_expr}, i64 0, i64 0), i8** {pname}"
            case _:
                return f"\tstore {llvm_type} {compiled_expr}, {llvm_type}* {pname}"
    
    def has_string(self, value):
        return value in self.strings
    
    def get_string_reg(self, value):
        return self.strings[value]
    
    def add_string(self, value, reg):
        self.strings[value] = reg
    
    def enter_block(self):
        self.context.append({})
    
    def exit_block(self):
        self.context.pop()

def first_traversal(emitter, node: Start):
    """
    This function is used to declare all variables and functions in the global scope.
    """
    for global_node in node.defs_or_decls:
        match global_node:
            case VarDefinition(vname, type_, expr) | ValDefinition(vname, type_, expr):
                emitter.decl_var(vname)
                llvm_type = plush_type_to_llvm_type(type_)
                pname = emitter.get_pointer_name(vname)
                val = compile(emitter, expr)

                if isinstance(type_, StringType):
                    str_reg = emitter.get_string_reg(expr.value)
                    str_len = len(expr.value) + 1
                    emitter << f"{pname} = dso_local global i8* getelementptr inbounds ([{str_len} x i8], [{str_len} x i8]* {str_reg}, i32 0, i32 0)"
                else:
                    emitter << f"{pname} = dso_local global {llvm_type} {val}"


from llvmlite import ir

def float_to_llvm(value):
    """ Convert float literals to LLVM float constants """
    return ir.Constant(ir.FloatType(), value).get_reference()

def get_array_llvm_type(type_):
    stars = "*"
    res_type = type_.type_
    while isinstance(res_type, ArrayType):
        stars += "*"
        res_type = res_type.type_
    return str(plush_type_to_llvm_type(res_type)) + stars

def plush_type_to_llvm_type(type_):
    if isinstance(type_, IntType):
        return ir.IntType(32)
    elif isinstance(type_, FloatType):
        return ir.FloatType()
    elif isinstance(type_, CharType):
        return ir.PointerType(ir.IntType(8))
    elif isinstance(type_, StringType):
        return ir.PointerType(ir.IntType(8))
    elif isinstance(type_, BooleanType):
        return ir.IntType(1)
    elif isinstance(type_, ArrayType):
        return get_array_llvm_type(type_)
    elif not type_:
        return ir.VoidType()
    else:
        raise ValueError(f"Unknown type {type_}")



def compile(emitter: Emitter, node):
    # first_traversal(emitter, node)
    # assert len(emitter.context) == 1
    match node:
        case Start( defs_or_decls ):
            first_traversal(emitter, node)
            predef_funcs_file = open("../pre_def_funcs.ll", "r")
            emitter << predef_funcs_file.read()
            

            for def_or_decl in defs_or_decls:
                compile(emitter, def_or_decl)

            return emitter.get_code()
        
        case ValDefinition(vname, type_, expr) | VarDefinition(vname, type_, expr):
            if emitter.is_in_global_context(): return

            emitter.decl_var(vname)

            llvm_type = plush_type_to_llvm_type(type_)
            pname = emitter.get_pointer_name(vname)
            emitter << f"\t{pname} = alloca {llvm_type}"

            emitter << emitter.get_llvm_code_to_store(expr, pname, llvm_type)
        case Assignment(vname, expr):
            pname = emitter.get_pointer_name(vname)
            llvm_type = plush_type_to_llvm_type(expr.type_)

            emitter << emitter.get_llvm_code_to_store(expr, pname, llvm_type)
        case ArrayPositionAssignment(name, indexes, expr):
            tmp_reg = "%" + emitter.get_temp()
            pname = emitter.get_pointer_name(name)

            stars = "*" * len(indexes)
            type_ = expr.type_
            while isinstance(type_, ArrayType):
                type_ = type_.type_
                stars += "*"

            llvm_type = plush_type_to_llvm_type(type_)

            emitter << f"\t{tmp_reg} = load {llvm_type}{stars}, {llvm_type}{stars}* {pname}"

            for index in indexes:
                index_value = compile(emitter, index)
                pos_ptr = f"%{name}idx" + emitter.get_temp()
                emitter << f"\t{pos_ptr} = getelementptr {llvm_type}, {llvm_type}* {tmp_reg}, i32 {index_value}"
                tmp_reg = "%" + emitter.get_temp()
                emitter << emitter.get_llvm_code_to_store(expr, pos_ptr, llvm_type)
        case If(cond, block):
            compiled_cond  = compile(emitter, cond)
            then_count = emitter.get_count()
            end_count = emitter.get_count()
            emitter << f"\tbr i1 {compiled_cond}, label %if_true{then_count}, label %if_end{end_count}"

            emitter << f"if_true{then_count}:"
            emitter.enter_block()
            for stmt in block:
                compile(emitter, stmt)
            emitter << f"\tbr label %if_end{end_count}"
            emitter.exit_block()

            emitter << f"if_end{end_count}:"

        case IfElse(cond, then_block, else_block):
            compiled_cond  = compile(emitter, cond)
            then_count = emitter.get_count()
            else_count = emitter.get_count()
            end_count = emitter.get_count()

            emitter << f"\tbr i1 {compiled_cond}, label %if_true{then_count}, label %else{else_count}"

            emitter << f"if_true{then_count}:"
            emitter.enter_block()
            for stmt in then_block:
                compile(emitter, stmt)
            emitter << f"\tbr label %if_end{end_count}"
            emitter.exit_block()

            emitter << f"else{else_count}:"
            emitter.enter_block()
            for stmt in else_block:
                compile(emitter, stmt)
            emitter << f"\tbr label %if_end{end_count}"
            emitter.exit_block()

            emitter << f"if_end{end_count}:"
        
        case While(cond, block):
            while_cond_count = emitter.get_count()
            while_body_count = emitter.get_count() 
            while_end_count = emitter.get_count()
            emitter << f"\tbr label %while_cond{while_cond_count}"

            emitter << f"while_cond{while_cond_count}:"
            compiled_cond = compile(emitter, cond)
            emitter << f"\tbr i1 {compiled_cond}, label %while_body{while_body_count}, label %while_end{while_end_count}"

            emitter << f"while_body{while_body_count}:"
            emitter.enter_block()
            for stmt in block:
                compile(emitter, stmt)
            emitter << f"\tbr label %while_cond{while_cond_count}"
            emitter.exit_block()

            emitter << f"while_end{while_end_count}:"

        case FunctionCall(name, args, type_):
            args_compiled = [(compile(emitter, arg),arg.type_) for arg in args]
            
            llvm_type = plush_type_to_llvm_type(type_)
            llvm_concrete_types = [ f"{plush_type_to_llvm_type(type_)}  {reg}" for reg, type_ in args_compiled]
            
            tmp_reg = ""
            
            if type_:
                tmp_reg = "%" + emitter.get_temp()
                emitter << f"\t{tmp_reg} = call {llvm_type} @{name}( {', '.join(llvm_concrete_types)} )"
            else:
                emitter << f"\tcall {llvm_type} @{name}( {', '.join(llvm_concrete_types)} )"
            return tmp_reg
        case FunctionDeclaration(name, params, type_):
            #TODO: pass?
            pass
        case FunctionDefinition(fname, params, type_, block):
            emitter.enter_block()
            llvm_params = ", ".join([f"{plush_type_to_llvm_type(param.type_)} %{param.name}" for param in params])
            param_allocation = []
            param_store = []

            return_type = plush_type_to_llvm_type(type_)
            emitter << f"define {return_type} @{fname}({llvm_params}) {{"

            # TODO: Add params
            for param in params:
                param_name, ptype_ = param.name, param.type_
                emitter.decl_var(param_name)
                llvm_type = plush_type_to_llvm_type(ptype_)
                pname = emitter.get_pointer_name(param_name)
                param_allocation.append(f"\t{pname} = alloca {llvm_type}")
                param_store.append(f"\tstore {llvm_type} %{param_name}, {llvm_type}* {pname}")
            
            if type_:
                # Add return assign
                emitter.decl_var(fname)
                ret_pname = emitter.get_pointer_name(fname)
                emitter << f"\t{ret_pname} = alloca {return_type}"
            if len(params) > 0:
                emitter << "\n".join(param_allocation)
                emitter << "\n".join(param_store)

            
            for stmt in block:
                compile(emitter, stmt)
            
            ret_str = "\tret void"
            if type_:
                temp_reg = "%" + emitter.get_temp()
                emitter << f"\t{temp_reg} = load {return_type}, {return_type}* {ret_pname}"
                ret_str = f"\tret {return_type} {temp_reg}"
            
            emitter << ret_str

            emitter << "}"
            emitter.exit_block()
        case Add(left, right, type_) | Sub(left, right, type_) | Mul(left, right, type_) |\
                Div(left, right, type_) | Mod(left, right, type_):
            l = compile(emitter, left)
            r = compile(emitter, right)
            pos_ptr = "%" + emitter.get_temp()
            operator = OPS[type(node)]
            llvm_type = plush_type_to_llvm_type(type_)

            if isinstance(type_, FloatType):
                operator = "f" + operator

            emitter << f"\t{pos_ptr} = {operator} {llvm_type} {l}, {r}"
            return pos_ptr
        case Power(base, exponent, type_):
            b = compile(emitter, base)
            e = compile(emitter, exponent)
            pos_ptr = "%" + emitter.get_temp()
            emitter << f"\t{pos_ptr} = call i32 @power_int(i32 {b}, i32 {e})"
            return pos_ptr
        case Or(left, right)| And(left,right) :
            l = compile(emitter, left)
            r = compile(emitter, right)

            operator = OPS[type(node)]
            pos_ptr = "%" + emitter.get_temp()
            emitter << f"\t{pos_ptr} = {operator} i1 {l}, {r}"
            return pos_ptr
        case LogicNot(expr):
            compiled_expr = compile(emitter, expr)
            pos_ptr = "%" + emitter.get_temp()
            emitter << f"\t{pos_ptr} = xor i1 {compiled_expr}, 1"
            return pos_ptr
        case UnaryMinus(expr):
            compiled_expr = compile(emitter, expr)
            pos_ptr = "%" + emitter.get_temp()
            emitter << f"\t{pos_ptr} = sub i32 0, {compiled_expr}"
            return pos_ptr
        case LessThan(left, right) | LessThanOrEqual(left, right) |\
                GreaterThan(left, right) | GreaterThanOrEqual(left, right) |\
                Equal(left, right) | NotEqual(left, right):
            l = compile(emitter, left)
            r = compile(emitter, right)
            pos_ptr = "%" + emitter.get_temp()
            operator = OPS[type(node)]
            emitter << f"\t{pos_ptr} = icmp {operator} i32 {l}, {r}"
            return pos_ptr
        case ArrayAccess(name, indexes, type_):
            tmp_reg = "%" + emitter.get_temp()
            pname = emitter.get_pointer_name(name)
            
            llvm_type = plush_type_to_llvm_type(type_)

            stars = "*" * len(indexes)
            while isinstance(type_, ArrayType):
                type_ = type_.type_
                stars += "*"
            array_type = f"{llvm_type}{stars}"
            emitter << f"\t{tmp_reg} = load {array_type}, {array_type}* {pname}"

            # N stars reduces from n to 1

            for index in indexes:
                stars = stars[0:-1]
                index_value = compile(emitter, index)
                pos_ptr = f"%{name}idx" + emitter.get_temp()
                emitter << f"\t{pos_ptr} = getelementptr {llvm_type}{stars}, {llvm_type}{stars}* {tmp_reg}, i32 {index_value}"
                tmp_reg = "%" + emitter.get_temp()
                emitter << f"\t{tmp_reg} = load {llvm_type}{stars}, {llvm_type}{stars}* {pos_ptr}"
            
            return tmp_reg

        case Id(vname, type_):
            tmp_reg = "%" + emitter.get_temp()
            pname = emitter.get_pointer_name(vname)

            llvm_type = plush_type_to_llvm_type(type_)
            emitter << f"\t{tmp_reg} = load {llvm_type}, {llvm_type}* {pname}"
            return tmp_reg
        case IntLit(value):
            return value
        case FloatLit(value):
            return float_to_llvm(float(value))
        case CharLit(value):
            return value
        case String(value):
            if emitter.has_string(value):
                return emitter.get_string_reg(value)

            id = emitter.get_count()
            str_name = f"@.pl_str_{id}"
            str_decl = f"""{str_name} = private unnamed_addr constant [{len(value)+1} x i8] c"{value}\\00" """
            emitter.lines.insert(0, str_decl)
            emitter.add_string(value, str_name)
            return str_name
        case BooleanLit(value):
            return value
        
        case _:
            raise TypeError(f"Unknown node type {node}")


if __name__ == "__main__":
    typed_tree = type_check_program("my_program.pl")
    e = Emitter()
    llvm_code = compile(e, typed_tree)
    print(llvm_code)
    with open("code.ll", "w") as f:
        f.write(llvm_code)
    import subprocess

    lib_flags = "-lm"
    # /usr/local/opt/llvm/bin/lli code.ll
    r = subprocess.call(
        # "llc code.ll && clang code.s -o code -no-pie && ./code",
        f"llc code.ll && gcc -c plush_functions.c && clang code.s plush_functions.o {lib_flags} -o code -no-pie && ./code",
        # "lli code.ll",
        shell=True,
    )
    print()

