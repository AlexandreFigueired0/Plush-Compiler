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
    Equal: "icmp eq",
    NotEqual: "icmp ne",
    LessThan: "icmp slt",
    LessThanOrEqual: "icmp sle",
    GreaterThan: "icmp sgt",
    GreaterThanOrEqual: "icmp sge",
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
    
def compile(emitter: Emitter, node):
    match node:
        case Start( defs_or_decls ):
            emitter << "declare i32 @printf(i8*, ...) #1"
            
            for def_or_decl in defs_or_decls:
                compile(emitter, def_or_decl)

            return emitter.get_code()
        
        case ValDefinition(vname, type_, expr) | VarDefinition(vname, type_, expr):
            emitter.decl_var(vname)
            llvm_type = TYPES[str(type_)]
            pname = emitter.get_pointer_name(vname)
            emitter << f"\t{pname} = alloca {llvm_type}"

            value = compile(emitter, expr)
            emitter << f"\tstore {llvm_type} {value}, {llvm_type}* {pname}"
        case If(cond, block):
            compiled_cond  = compile(emitter, cond)
            true_count = emitter.get_count()
            false_count = emitter.get_count()
            emitter << f"\tbr i1 {compiled_cond}, label %if_true{true_count}, label %if_false{false_count}"
            emitter << "\n"
            emitter << f"if_true{true_count}:"
            emitter.enter_block()
            for stmt in block:
                compile(emitter, stmt)
            emitter.exit_block()
            emitter << "\n"


        case FunctionCall(name, args, type_):
            if name == "print_int":
                arg = args[0]
                id = emitter.get_temp()
                str_name = f"@.plush_str_{id}"
                str_decl = f"""{str_name} = private  constant [4 x i8] c"%d\\0A\\00" """
                emitter.lines.insert(0, str_decl)

                val = compile(emitter,arg)
                nreg = "%" + emitter.get_temp()
                emitter << f"""\t{nreg} = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* {str_name}, i64 0, i64 0), i32 {val})"""
                return nreg
        case FunctionDeclaration(name, params, type_):
            pass
        case FunctionDefinition(name, params, type_, block):
            emitter.enter_block()
            # TODO: Add params
            for param in params:
                pname, ptype_ = param.name, param.type_S
                emitter.decl_var(pname)
                llvm_type = TYPES[str(ptype_)]
                pname = emitter.get_pointer_name(pname)
                emitter << f"\t{pname} = alloca {llvm_type}"

            return_type = TYPES[str(type_)]
            emitter << f"define {return_type} @{name}() {{"
            
            for stmt in block:
                compile(emitter, stmt)
            
            ret_str = None
            if type_:
                ret_str = f"\tret {return_type} 0"
            else:
                ret_str = f"\tret {return_type}"

            emitter << ret_str
            emitter << "}"
            emitter.exit_block()
        case Add(left, right, type_) | Sub(left, right, type_) | Mul(left, right, type_) |\
                Div(left, right, type_) | Mod(left, right, type_):
            l = compile(emitter, left)
            r = compile(emitter, right)
            tmp_ptr = "%" + emitter.get_temp()
            operator = OPS[type(node)]
            emitter << f"   {tmp_ptr} = {operator} i32 {l}, {r}"
            return tmp_ptr
        case Power(left, right, type_):
            raise NotImplementedError("Power operator not implemented")
        case Or(left, right) | And(left, right):
            raise NotImplementedError("Logical operators not implemented")
        case LogicNot(expr):
            raise NotImplementedError("Not operator not implemented")
        case LessThan(left, right) | LessThanOrEqual(left, right) |\
                GreaterThan(left, right) | GreaterThanOrEqual(left, right):
            l = compile(emitter, left)
            r = compile(emitter, right)
            tmp_ptr = "%" + emitter.get_temp()
            operator = OPS[type(node)]
            emitter << f"\t{tmp_ptr} = {operator} i32 {l}, {r}"
            return tmp_ptr
        case Id(vname):
            reg = "%" + emitter.get_temp()
            pname = emitter.get_pointer_name(vname)
            emitter << f"   {reg} = load i32, i32* {pname}"
            return reg
        case IntLit(value):
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

    # /usr/local/opt/llvm/bin/lli code.ll
    r = subprocess.call(
        "llc code.ll && clang code.s -o code -no-pie && ./code",
        # "lli code.ll",
        shell=True,
    )