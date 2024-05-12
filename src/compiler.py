from ast_nodes import *
from type_checker import type_check_program

TYPES = {
    "int": "i32",
    "float": "f32",
    "char": "i8",
    "string": "i8",
    "boolean": "i1",
    "None": "void"
}

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

    def decl_var(self, name):
        self.context[-1][name] = self.get_count()

    def get_count(self):
        self.count += 1
        return self.count

    def get_temp(self):
        id = self.get_count()
        return f"tmp_{id}"

    def __lshift__(self, v):
        self.lines.append(v)

    def get_code(self):
        return "\n".join(self.lines)

    def get_pointer_name(self, vname):
        for ctx in reversed(self.context):
            if vname in ctx:
                return f"%{vname}{ctx[vname]}"
        raise ValueError(f"Variable {vname} not found in context")
    
    def enter_block(self):
        self.context.append({})
    
    def exit_block(self):
        self.context.pop()

def first_traversal(emitter, node: Start):
    """
    This function is used to declare all variables and functions in the global scope.
    Also, it will declare all strings and arrays used in the program.
    """
    for global_node in node.defs_or_decls:
        match global_node:
            case VarDefinition(vname, type_, expr):
                emitter.decl_var(vname)

        

def compile(emitter: Emitter, node):
    # first_traversal(emitter, node)
    # assert len(emitter.context) == 1
    match node:
        case Start( defs_or_decls ):
            predef_funcs_file = open("../pre_def_funcs.ll", "r")
            emitter << predef_funcs_file.read()
            
            for def_or_decl in defs_or_decls:
                compile(emitter, def_or_decl)

            return emitter.get_code()
        
        case ValDefinition(vname, type_, expr) | VarDefinition(vname, type_, expr):
            emitter.decl_var(vname)

            llvm_type = None
            if isinstance(type_, ArrayType):
                llvm_type
            else:
                llvm_type = TYPES[str(type_)]
            pname = emitter.get_pointer_name(vname)
            emitter << f"\t{pname} = alloca {llvm_type}"

            value = compile(emitter, expr)
            emitter << f"\tstore {llvm_type} {value}, {llvm_type}* {pname}"
        case Assignment(vname, expr):
            pname = emitter.get_pointer_name(vname)
            value = compile(emitter, expr)
            llvm_type = TYPES[str(expr.type_)]
            emitter << f"\tstore {llvm_type} {value}, {llvm_type}* {pname}"
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
            llvm_type = None
            if isinstance(type_, ArrayType):
                pass
            else:
                llvm_type = TYPES[str(type_)]
            llvm_concrete_types = [ f"{TYPES[str(type_)]}  {reg}" for reg, type_ in args_compiled]
            
            reg = ""
            
            if type_:
                reg = "%" + emitter.get_temp()
                emitter << f"\t{reg} = call {llvm_type} @{name}( {', '.join(llvm_concrete_types)} )"
            else:
                emitter << f"\tcall {llvm_type} @{name}( {', '.join(llvm_concrete_types)} )"
            return reg
        case FunctionDeclaration(name, params, type_):
            #TODO: pass?
            pass
        case FunctionDefinition(fname, params, type_, block):
            emitter.enter_block()
            llvm_params = ", ".join([f"{TYPES[str(param.type_)]} %{param.name}" for param in params])
            param_allocation = []
            param_load = []
            return_type = TYPES[str(type_)]
            emitter << f"define {return_type} @{fname}({llvm_params}) {{"

            # TODO: Add params
            for param in params:
                param_name, ptype_ = param.name, param.type_
                emitter.decl_var(param_name)
                llvm_type = TYPES[str(ptype_)]
                pname = emitter.get_pointer_name(param_name)
                param_allocation.append(f"\t{pname} = alloca {llvm_type}")
                param_load.append(f"\tstore {llvm_type} %{param_name}, {llvm_type}* {pname}")
            
            if type_:
                # Add return assign
                emitter.decl_var(fname)
                ret_pname = emitter.get_pointer_name(fname)
                emitter << f"\t{ret_pname} = alloca {return_type}"
            emitter << "\n".join(param_allocation)
            emitter << "\n".join(param_load)

            
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
            tmp_ptr = "%" + emitter.get_temp()
            operator = OPS[type(node)]
            llvm_type = TYPES[str(type_)]
            emitter << f"\t{tmp_ptr} = {operator} {llvm_type} {l}, {r}"
            return tmp_ptr
        case Power(base, exponent, type_):
            b = compile(emitter, base)
            e = compile(emitter, exponent)
            tmp_ptr = "%" + emitter.get_temp()
            emitter << f"\t{tmp_ptr} = call i32 @power_int(i32 {b}, i32 {e})"
            return tmp_ptr
        case Or(left, right)| And(left,right) :
            l = compile(emitter, left)
            r = compile(emitter, right)

            operator = OPS[type(node)]
            tmp_ptr = "%" + emitter.get_temp()
            emitter << f"\t{tmp_ptr} = {operator} i1 {l}, {r}"
            return tmp_ptr
        case LogicNot(expr):
            compiled_expr = compile(emitter, expr)
            tmp_ptr = "%" + emitter.get_temp()
            emitter << f"\t{tmp_ptr} = xor i1 {compiled_expr}, 1"
            return tmp_ptr
        case UnaryMinus(expr):
            compiled_expr = compile(emitter, expr)
            tmp_ptr = "%" + emitter.get_temp()
            emitter << f"\t{tmp_ptr} = sub i32 0, {compiled_expr}"
            return tmp_ptr
        case LessThan(left, right) | LessThanOrEqual(left, right) |\
                GreaterThan(left, right) | GreaterThanOrEqual(left, right):
            l = compile(emitter, left)
            r = compile(emitter, right)
            tmp_ptr = "%" + emitter.get_temp()
            operator = OPS[type(node)]
            emitter << f"\t{tmp_ptr} = icmp {operator} i32 {l}, {r}"
            return tmp_ptr
        case Id(vname, type_):
            reg = "%" + emitter.get_temp()
            pname = emitter.get_pointer_name(vname)
            llvm_type = TYPES[str(type_)]
            emitter << f"\t{reg} = load {llvm_type}, {llvm_type}* {pname}"
            return reg
        case IntLit(value):
            return value
        case FloatLit(value):
            return value
        case CharLit(value):
            return value
        case String(value):
            return value
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
        f"llc code.ll && gcc -c plush_functions.c && clang code.s plush_functions.o {lib_flags} -o code && ./code",
        # "lli code.ll",
        shell=True,
    )
    print()