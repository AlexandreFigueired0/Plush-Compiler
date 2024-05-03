from ast_nodes import *
from type_checker import type_check_program

types = {
    "int": "i32",
    "float": "f32",
    "char": "i8",
    "string": "i8",
    "boolean": "i1",
    "None": "i32"
}

class Emitter(object):
    def __init__(self):
        self.count = 0
        self.lines = []

    def get_count(self):
        self.count += 1
        return self.count

    def get_id(self):
        id = self.get_count()
        return f"cas_{id}"

    def __lshift__(self, v):
        self.lines.append(v)

    def get_code(self):
        return "\n".join(self.lines)

    def get_pointer_name(self, n):
        return f"%ptr_{n}"
    
def compile(emitter: Emitter, node):
    match node:
        case Start( defs_or_decls ):
            emitter << "declare i32 @printf(i8*, ...) #1"
            
            for def_or_decl in defs_or_decls:
                compile(emitter, def_or_decl)

            return emitter.get_code()
        
        case ValDefinition(vname, type_, expr):
            llvm_type = types[str(type_)]
            pname = emitter.get_pointer_name(vname)
            emitter << f"\t{pname} = alloca {llvm_type}"

            value = compile(emitter, expr)
            emitter << f"\tstore {llvm_type} {value}, {llvm_type}* {pname}"
        case FunctionCall(name, args, type_):
            if name == "print_int":
                arg = args[0]
                id = emitter.get_id()
                str_name = f"@.casual_str_{id}"
                str_decl = f"""{str_name} = private unnamed_addr constant [4 x i8] c"%d\\0A\\00", align 1"""
                emitter.lines.insert(0, str_decl)

                val = compile(emitter,arg)
                nreg = "%" + emitter.get_id()
                emitter << f"""\t{nreg} = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* {str_name}, i64 0, i64 0), i32 {val})"""
                return nreg
        case FunctionDeclaration(name, params, type_):
            pass
        case FunctionDefinition(name, params, type_, block):
            return_type = types[str(type_)]
            emitter << f"define {return_type} @{name}() {{"
            
            for stmt in block:
                compile(emitter, stmt)
            
            ret_str = None
            if type_:
                ret_str = f"\tret {return_type} 0"
            else:
                ret_str = f"\tret {return_type} 0"

            emitter << ret_str
            emitter << "}"
        case Id(vname):
            reg = "%" + emitter.get_id()
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
        # "llc code.ll && clang code.s -o code && ./code",
        "lli code.ll",
        shell=True,
    )