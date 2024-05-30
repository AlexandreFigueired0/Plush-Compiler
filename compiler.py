from ast_nodes import *
from type_checker import type_check_program
import sys



class Emitter(object):
    def __init__(self):
        self.count = 0
        self.lines = []
        # will contain the id of the var in this scope
        self.context = [{}]

        # will cotain the register name for the static strings
        self.strings = {}

        self.functions = set()

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

    def has_function(self, name):
        return name in self.functions
    
    def add_function(self, name):
        self.functions.add(name)

    
    def enter_block(self):
        self.context.append({})
    
    def exit_block(self):
        self.context.pop()

def first_traversal(emitter, node: Start):
    """
    This function is used to declare all variables in the global scope.
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
    stars = ""
    res_type = type_
    while isinstance(res_type, ArrayType):
        stars += "*"
        res_type = res_type.type_
    return str(plush_type_to_llvm_type(res_type)) + stars

def plush_type_to_llvm_type(type_):
    if not type_: return ir.VoidType()

    match type_:
        case IntType():
            return ir.IntType(32)
        case FloatType():
            return ir.FloatType()
        case CharType():
            return ir.IntType(8)
        case StringType():
            return ir.PointerType(ir.IntType(8))
        case BooleanType():
            return ir.IntType(1)
        case ArrayType(_):
            return get_array_llvm_type(type_)
        case _:
            raise ValueError(f"Unknown type {type_}")

def get_llvm_operation(node):
    match node:
        case Add(l,r,t):
            return "add" if t == IntType() else "fadd"
        case Sub(l,r,t):
            return "sub" if t == IntType() else "fsub"
        case Mul(l,r,t):
            return "mul" if t == IntType() else "fmul"
        case Div(l,r,t):
            return "sdiv" if t == IntType() else "fdiv"
        case Mod(l,r,t):
            return "srem"
        case Equal(l,r):
            return "eq" if l.type_ == IntType() else "oeq"
        case NotEqual(l,r):
            return "ne" if l.type_ == IntType() else "une"
        case LessThan(l,r):
            return "slt" if l.type_ == IntType() else "olt"
        case LessThanOrEqual(l,r):
            return "sle" if l.type_ == IntType() else "ole"
        case GreaterThan(l,r):
            return "sgt" if l.type_ == IntType() else "ogt"
        case GreaterThanOrEqual(l,r):
            return "sge" if l.type_ == IntType() else "oge"
        case And(l,r):
            return "and"
        case Or(l,r):
            return "or"
        case _:
            raise ValueError(f"Unknown node {node}")
    

def compile(emitter: Emitter, node):
    # first_traversal(emitter, node)
    # assert len(emitter.context) == 1
    match node:
        case Start( defs_or_decls ):
            first_traversal(emitter, node)
            predef_funcs_file = open("pre_def_funcs.ll", "r")
            emitter << predef_funcs_file.read()
            

            for def_or_decl in defs_or_decls:
                if isinstance(def_or_decl, ValDefinition) or isinstance(def_or_decl, VarDefinition):
                    continue
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
            array_ptr = "%" + emitter.get_temp()
            pname = emitter.get_pointer_name(name)

            stars = "*" * len(indexes)
            type_ = expr.type_
            while isinstance(type_, ArrayType):
                type_ = type_.type_
                stars += "*"

            llvm_type = plush_type_to_llvm_type(type_)

            emitter << f"\t{array_ptr} = load {llvm_type}{stars}, {llvm_type}{stars}* {pname}"

            for index in indexes:
                stars = stars[0:-1]
                index_value = compile(emitter, index)
                pos_ptr = f"%{name}_idx_{emitter.get_count()}"
                emitter << f"\t{pos_ptr} = getelementptr {llvm_type}{stars}, {llvm_type}{stars}* {array_ptr}, i32 {index_value}"
                array_ptr = "%" + emitter.get_temp()
                emitter << f"\t{array_ptr} = load {llvm_type}{stars}, {llvm_type}{stars}* {pos_ptr}"
            
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
            args_compiled = []

            for arg in args:
                # If the argument is a string, we need to create a pointer to it
                if isinstance(arg, String):
                    str_name = compile(emitter, arg)
                    temp_reg = "%" + emitter.get_temp()
                    emitter << f"\t{temp_reg} = alloca i8*"
                    str_len = len(arg.value) + 1
                    emitter << f"\tstore i8* getelementptr inbounds ([{str_len} x i8], [{str_len} x i8]* {str_name}, i64 0, i64 0), i8** {temp_reg}"
                    ret_reg = f"%" + emitter.get_temp()
                    emitter << f"\t{ret_reg} = load i8*, i8** {temp_reg}"
                    args_compiled.append((ret_reg, StringType()))
                else:
                    args_compiled.append((compile(emitter, arg),arg.type_))
            
            llvm_type = plush_type_to_llvm_type(type_)
            llvm_concrete_types = [ f"{plush_type_to_llvm_type(type_)}  {reg}" for reg, type_ in args_compiled]
            
            call_ret_reg = ""
            llvm_function_call = f"call {llvm_type} @{name}( {', '.join(llvm_concrete_types)} )"
            
            if type_:
                call_ret_reg = f"%{name}_{emitter.get_count()}"
                emitter << f"\t{call_ret_reg} = {llvm_function_call}"
            else:
                emitter << f"\t{llvm_function_call}"
            return call_ret_reg
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
            ret_reg = "%" + emitter.get_temp()
            operator = get_llvm_operation(node)
            llvm_type = plush_type_to_llvm_type(type_)

            emitter << f"\t{ret_reg} = {operator} {llvm_type} {l}, {r}"
            return ret_reg
        case Power(base, exponent, type_):
            b = compile(emitter, base)
            e = compile(emitter, exponent)
            ret_reg = "%" + emitter.get_temp()

            if isinstance(type_, FloatType):
                emitter << f"\t{ret_reg} = call float @power_float(float {b}, float {e})"
            else:
                emitter << f"\t{ret_reg} = call i32 @power_int(i32 {b}, i32 {e})"
            return ret_reg
        case Or(left, right)| And(left,right) :
            l = compile(emitter, left)
            r = compile(emitter, right)

            operator = get_llvm_operation(node)
            ret_reg = "%" + emitter.get_temp()
            emitter << f"\t{ret_reg} = {operator} i1 {l}, {r}"
            return ret_reg
        case LogicNot(expr):
            compiled_expr = compile(emitter, expr)
            ret_reg = "%" + emitter.get_temp()
            emitter << f"\t{ret_reg} = xor i1 {compiled_expr}, 1"
            return ret_reg
        case UnaryMinus(expr):
            compiled_expr = compile(emitter, expr)
            ret_reg = "%" + emitter.get_temp()
            llvm_type = plush_type_to_llvm_type(expr.type_)

            if isinstance(expr, FloatLit) or isinstance(expr, IntLit):
                return f"-{expr.value}"
            elif isinstance(expr.type_, FloatType):
                emitter << f"\t{ret_reg} = fsub {llvm_type} 0.0, {compiled_expr}"
            else:
                emitter << f"\t{ret_reg} = sub {llvm_type} 0, {compiled_expr}"
            return ret_reg
        case LessThan(left, right) | LessThanOrEqual(left, right) |\
                GreaterThan(left, right) | GreaterThanOrEqual(left, right) |\
                Equal(left, right) | NotEqual(left, right):
            l = compile(emitter, left)
            r = compile(emitter, right)
            ret_reg = "%" + emitter.get_temp()
            operator = get_llvm_operation(node)
            llvm_cmp = "icmp" if isinstance(left.type_, IntType) else "fcmp"
            llvm_type = plush_type_to_llvm_type(left.type_)
            emitter << f"\t{ret_reg} = {llvm_cmp} {operator} {llvm_type} {l}, {r}"
            return ret_reg
        case ArrayAccess(name, indexes, type_) | FunctionCallArrayAccess(name, indexes, type_):
            llvm_type = plush_type_to_llvm_type(type_)
            stars = "*" * len(indexes)
            ret_reg = None

            if isinstance(node, ArrayAccess):
                pname = emitter.get_pointer_name(name)
                if isinstance(type_, ArrayType):
                    type_ = type_.type_
                    while isinstance(type_, ArrayType):
                        stars += "*"
                ret_reg = "%" + emitter.get_temp()
                array_type = f"{llvm_type}{stars}"
                emitter << f"\t{ret_reg} = load {array_type}, {array_type}* {pname}"

            else: ## name is a function call
                ret_reg = compile(emitter, name)

            name = name.name if isinstance(name, FunctionCall) else name


            # N stars reduces from n to 1

            for index in indexes:
                stars = stars[0:-1]
                index_value = compile(emitter, index)
                pos_ptr = f"%{name}_idx_{emitter.get_count()}"
                emitter << f"\t{pos_ptr} = getelementptr {llvm_type}{stars}, {llvm_type}{stars}* {ret_reg}, i32 {index_value}"
                ret_reg = "%" + emitter.get_temp()
                emitter << f"\t{ret_reg} = load {llvm_type}{stars}, {llvm_type}{stars}* {pos_ptr}"
            
            return ret_reg

        case Id(vname, type_):
            ret_reg = "%" + emitter.get_temp()
            pname = emitter.get_pointer_name(vname)

            llvm_type = plush_type_to_llvm_type(type_)
            emitter << f"\t{ret_reg} = load {llvm_type}, {llvm_type}* {pname}"
            return ret_reg
        case IntLit(value):
            return value
        case FloatLit(value):
            return float_to_llvm(float(value))
        case CharLit(value):
            return ord(value)
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
    fname = sys.argv[1]
    typed_tree = type_check_program(fname)
    e = Emitter()
    llvm_code = compile(e, typed_tree)
    # print(llvm_code)
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

