import sys
from src.pl_parser.ast_nodes import *
from src.pl_parser.plush_parser import parse_plush

class Context():
    def __init__(self):
        self.stack = [{}]
        self.functions = {}
    
    def get_type(self, name):
        for scope in self.stack[::-1]:
            if name in scope:
                return scope[name]
        raise TypeError(f"Variable {name} doesn't exist")
    
    def set_type(self, name, value, can_define=True):
        scope = self.stack[-1]
        scope[name] = (value, can_define)
    
    def has_function(self, name):
        return name in self.functions

    def has_function(self, name):
        return name in self.functions

    def add_function(self,f_content, can_define=True):
        self.functions[f_content[0]] = (f_content, can_define)
    
    def get_function(self, name):
        if name in self.functions:
            return self.functions[name]
        raise TypeError(f"Function {name} doesn't exist")

    def has_var(self, name):
        for scope in self.stack[::-1]:
            if name in scope:
                return True
        return False
    
    def has_var_in_current_scope(self, name):
        return name in self.stack[-1]
    
    def enter_block(self):
        self.stack.append({})
    
    def exit_block(self):
        self.stack.pop()

def add_pre_def_funcs(ctx: Context):
    ctx.add_function(("print_int",[ValParam(name="x", type_ = IntType())],None), False)
    ctx.add_function(("print_float",[ValParam(name="x", type_ = FloatType())],None), False)
    ctx.add_function(("print_string",[ValParam(name="s", type_ = StringType())],None), False)
    ctx.add_function(("print_char",[ValParam(name="c", type_ = CharType())],None), False)
    ctx.add_function(("print_boolean",[ValParam(name="x", type_ = BooleanType())],None), False)
    ctx.add_function(("print_int_array",[ValParam(name="a", type_ = ArrayType(type_=IntType())), ValParam(name="size", type_=IntType())],None), False)
    ctx.add_function(("print_float_array",[ValParam(name="a", type_ = ArrayType(type_=FloatType())), ValParam(name="size", type_=IntType())],None), False)
    ctx.add_function(("print_string_array",[ValParam(name="a", type_ = ArrayType(type_=StringType())), ValParam(name="size", type_=IntType())],None), False)
    ctx.add_function(("print_char_array",[ValParam(name="a", type_ = ArrayType(type_=CharType())), ValParam(name="size", type_=IntType())],None), False)
    ctx.add_function(("print_boolean_array",[ValParam(name="a", type_ = ArrayType(type_=BooleanType())), ValParam(name="size", type_=IntType())],None), False)
    ctx.add_function(("string_to_char_array",[ValParam(name="s", type_ = StringType())],ArrayType(type_=CharType(), text = "[char]")), False)
    ctx.add_function(("get_int_array",[ValParam(name="size", type_ = IntType())],ArrayType(type_=IntType(), text="[int]")), False)
    ctx.add_function(("get_string_array",[ValParam(name="size", type_ = IntType())],ArrayType(type_=StringType(), text="[string]")), False)
    ctx.add_function(("get_char_array",[ValParam(name="size", type_ = IntType())],ArrayType(type_=CharType(), text="[char]")), False)
    ctx.add_function(("get_boolean_array",[ValParam(name="size", type_ = IntType())],ArrayType(type_=BooleanType(), text="[boolean]")), False)
    ctx.add_function(("get_int_matrix",[ValParam(name="rows", type_ = IntType()), ValParam(name="cols", type_ = IntType())],ArrayType(type_=ArrayType(type_=IntType()), text="[[int]]")), False)
    ctx.add_function(("get_float_matrix",[ValParam(name="rows", type_ = IntType()), ValParam(name="cols", type_ = IntType())],ArrayType(type_=ArrayType(type_=FloatType()), text="[float]")), False)
    ctx.add_function(("get_string_matrix",[ValParam(name="rows", type_ = IntType()), ValParam(name="cols", type_ = IntType())],ArrayType(type_=ArrayType(type_=StringType()), text="[[string]]")), False)
    ctx.add_function(("get_char_matrix",[ValParam(name="rows", type_ = IntType()), ValParam(name="cols", type_ = IntType())],ArrayType(type_=ArrayType(type_=CharType()), text="[[char]]")), False)
    ctx.add_function(("get_boolean_matrix",[ValParam(name="rows", type_ = IntType()), ValParam(name="cols", type_ = IntType())],ArrayType(type_=ArrayType(type_=BooleanType()), text="[[boolean]]")), False)

def gather_global_vars_and_funcs(ctx: Context, node):
    for global_node in node.defs_or_decls:
        match global_node:
            # case VarDefinition(vname, type_, expr):
            #     ctx.set_type(vname, type_)
            # case ValDefinition(vname, type_, expr):
            #     ctx.set_type(vname, type_, False)
            case FunctionDeclaration(_,_,_,_,_,name, params, type_):
                if ctx.has_function(name):
                    raise TypeError(f"Function {name} already declared")
                
                ctx.add_function(name, (name,params,type_))

            case FunctionDefinition(_,_,_,_,_,name, params, type_, block):
                if ctx.has_function(name) and ctx.get_function(name)[1] == False:
                    raise TypeError(f"Function {name} already defined")
                
                ctx.add_function((name,params,type_), False)
            case _:
                pass

def type_check(ctx : Context, node) -> bool:
    match node:
        case Start(defs_or_decls):
            add_pre_def_funcs(ctx)

            gather_global_vars_and_funcs(ctx, node)

            for def_or_decl in defs_or_decls:
                type_check(ctx, def_or_decl)
            return node
        case ValDefinition(_,_,_,_,_,name, type_, expr) | VarDefinition(_,_,_,_,_,name, type_, expr):

            # Check if variable is already declared
            if ctx.has_var_in_current_scope(name):
                show_simple_error(node, f"Error: Variable {name} already declared" )
            
            expr_type = type_check(ctx, expr)
            # floats can be assigned with ints?
            if type_ != expr_type :
                show_mismatch_error(node, type_, expr, f"Error: Type mismatch for variable {name}, expected {type_.text} but got {expr_type.text}")
            
            # If its a val, then cant be redefined
            ctx.set_type(name, type_, not isinstance(node, ValDefinition))
        case Assignment(_,_,_,_,_,name, expr):
            #TODO: Check if variable is already declared
            if not ctx.has_var(name):
                show_simple_error(node, f"Error: Variable {name} doesn't exist" )
            
            var_type,can_define = ctx.get_type(name)

            if not can_define:
                show_simple_error(node, f"Variable {name} is immutable" )

            expr_type = type_check(ctx, expr)
            if var_type != expr_type:
                show_simple_error(node, f"Error: Type mismatch for variable {name}, expected {var_type.text} but got {expr_type.text}" )
            
        case ArrayPositionAssignment(_,_,_,_,_,name, indexes, expr):
            if not ctx.has_var(name):
                show_simple_error(node, f"Variable {name} doesn't exist" )
            
            var_type, _ = ctx.get_type(name)

            
            #Check if the indexes are valid and go deeper in the type
            res_type = var_type
            for index in indexes:
                index_type = type_check(ctx, index)
                if index_type != IntType():
                    show_simple_error(node, f"Error: Type mismatch in {node.text}, index must be of type int but found {index_type}" )
                
                if not isinstance(res_type, ArrayType):
                    show_simple_error(node, f"Error: Type mismatch in {node.text}, expected array but got {res_type.text}")

                res_type = res_type.type_
            
            expr_type = type_check(ctx, expr)
            if res_type != expr_type:
                show_simple_error(node, f"Error: Type mismatch in {node.text}, expected {res_type} but got {res_type.text}")

        case Sub(_,_,_,_,_,_,left, right) | Mul(_,_,_,_,_,_,left, right) | Div(_,_,_,_,_,_,left, right) | Mod(_,_,_,_,_,_,left, right) | \
            Power(_,_,_,_,_,_,left, right) | Add(_,_,_,_,_,_,left, right):
        
            left_type = type_check(ctx, left)
            right_type = type_check(ctx, right)

            wrong_type = left_type if left_type not in [IntType(), FloatType()] else right_type
            if wrong_type not in [IntType(), FloatType()]:
                raise TypeError(f"Line {node.line}: Type mismatch in {node}, both operands must be both of numerical type but found {wrong_type}")

            if left_type != right_type:
                raise TypeError(f"Line {node.line}: Type mismatch in {node}, both operands must be both of the same type but found {left_type} and {right_type}")

            # Mod only accepts int
            if isinstance(node,Mod) and left_type != IntType():
                raise TypeError(f"Line {node.line}: Type mismatch in {node}, both operands must be of type int but found {left_type}")
            
            node.type_ = left_type
            return left_type
        
        case Or(_,_,_,_,_,_,left, right) | And(_,_,_,_,_,_,left, right):
            
            left_type = type_check(ctx, left)
            right_type = type_check(ctx, right)

            wrong_type = left_type if left_type != BooleanType() else right_type
            if wrong_type != BooleanType():
                raise TypeError(f"Line {node.line}: Type mismatch in {node}, both operands must be of type boolean but found {wrong_type}")
            
            return BooleanType()
        
        case Equal(_,_,_,_,_,_,left, right) | NotEqual(_,_,_,_,_,_,left, right):
            
            left_type = type_check(ctx, left)
            right_type = type_check(ctx, right)

            if left_type != right_type:
                raise TypeError(f"Line {node.line}: Type mismatch in {node}, both operands must be of the same type but found {left_type} and {right_type}")
            
            return BooleanType()
        
        case GreaterThan(_,_,_,_,_,_,left, right) | GreaterThanOrEqual(_,_,_,_,_,_,left, right) | \
            LessThan(_,_,_,_,_,_,left, right) | LessThanOrEqual(_,_,_,_,_,_,left, right):

            left_type = type_check(ctx, left)
            right_type = type_check(ctx, right)

            wrong_type = left_type if left_type not in [IntType(), FloatType()] else right_type
            if wrong_type not in [IntType(), FloatType()]:
                raise TypeError(f"Line {node.line}: Type mismatch in {node}, both operands must be both of numerical type but found {wrong_type}")
            
            if left_type != right_type:
                raise TypeError(f"Line {node.line}: Type mismatch in {node}, both operands must be both of the same type but found {left_type} and {right_type}")
            
            return BooleanType()

        case UnaryMinus(_,_,_,_,_,_,expr):
            expr_type = type_check(ctx, expr)
            if expr_type not in [IntType(), FloatType()]:
                raise TypeError(f"Line {node.line}: Type mismatch in {node}, operand must be a number but found {expr_type}")
            
            node.type_ = expr_type
            return expr_type
        
        case LogicNot(_,_,_,_,_,_,expr):
            expr_type = type_check(ctx, expr)
            if expr_type != BooleanType():
                raise TypeError(f"Line {node.line}: Type mismatch in {node}, operand must be of type boolean but found {expr_type}")
            return BooleanType()
            
        case ArrayAccess(_,_,_,_,_,_,name, indexes) | FunctionCallArrayAccess(_,_,_,_,_,_,name, indexes):
            res_type = None
            if isinstance(name, FunctionCall):
                if not ctx.has_function(name.name):
                    show_simple_error(name, f"Error: Function {name.name} doesn't exist" )

                res_type = type_check(ctx, name)
            else:
                if not ctx.has_var(name):
                    show_simple_error(node, f"Error: Variable {name} doesn't exist" )
                
                var_type,_ = ctx.get_type(name)

                res_type = var_type

            #Check if the indexes are valid and go deeper in the type
            for index in indexes:
                index_type = type_check(ctx, index)
                if index_type != IntType():
                    show_simple_error(node, f"Error: Type mismatch in {node.text}, index must be of type int but found {index_type.text}" )
                
                if not isinstance(res_type, ArrayType):
                    show_simple_error(node, f"Error: Type mismatch in {node.text}, expected array type but got {res_type.text}" )
                res_type = res_type.type_
            
            # TODO: Access array, so return the type of the elem accessed
            node.type_ = res_type
            return res_type

        case If(_,_,_,_,_,condition, block):
            condition_type = type_check(ctx, condition)
            if condition_type != BooleanType():
                show_simple_error(condition, f"Error: Type mismatch in if condition, condition must be of type boolean but found {condition_type.text}" )
            
            #TODO: entr block?
            ctx.enter_block()
            for statement in block:
                type_check(ctx, statement)
            ctx.exit_block()

        case IfElse(_,_,_,_,_,condition, block, else_block):
            condition_type = type_check(ctx, condition)
            if condition_type != BooleanType():
                show_simple_error(condition, f"Error: Type mismatch in if condition, condition must be of type boolean but found {condition_type.text}" )
            
            #TODO: entr block?
            ctx.enter_block()
            for statement in block:
                type_check(ctx, statement)
            ctx.exit_block()

            ctx.enter_block()
            for statement in else_block:
                type_check(ctx, statement)
            ctx.exit_block()
        
        case While(_,_,_,_,_,condition, block):
            condition_type = type_check(ctx, condition)
            if condition_type != BooleanType():
                show_simple_error(condition, f"Error: Type mismatch in if condition, condition must be of type boolean but found {condition_type.text}" )
            
            #TODO: entr block?
            ctx.enter_block()
            for statement in block:
                type_check(ctx, statement)
            ctx.exit_block()
        
        #TODO: Check if the function exists
        #TODO: Check if the arguments are correct
        #TODO: Check if the return type is correct
        case FunctionCall(_,_,_,_,_,_,name, given_args):
            f_context,_ = ctx.get_function(name)
            
            name, params, type_ = f_context
            # TODO: Check if the number of arguments is correct
            if len(params) != len(given_args):
                show_simple_error(node, f"Error: Function {name} expects {len(params)} arguments but got {len(given_args)}" )
            
            for i, arg in enumerate(given_args):
                arg_type = type_check(ctx, arg)
                if arg_type != params[i].type_:
                    show_simple_error(node, f"Error: Type mismatch in {node.text} parameters, expected {f_context[1][i].type_.text} but got {arg_type.text}" )
            node.type_ = f_context[2]
            return f_context[2]

        case FunctionDeclaration(_,_,_,_,_,name, params, type_):

            
            f_context = (name,[],type_)
            for p in params:
                f_context[1].append(p)
            ctx.add_function(f_context)

        case FunctionDefinition(_,_,_,_,_,name, params, type_, block):
            f_context = (name,params,type_)

            # Function declared, but not defined
            # TODO: Check if the arguments are correct, type and immut modifiers
            if ctx.has_function(name) and ctx.get_function(name)[1] == True:
                f_declared,_ = ctx.get_function(name) # 0: name; 1: params; 2: type

                if len(f_declared[1]) != len(params):
                    print(f"Error: Function {name} expects {len(f_declared[1])} arguments but got {len(params)}" )
                    print(f"line {node.line}: {node.text}")
                    sys.exit(1)
                
                for i, p in enumerate(params):
                    if p.type_ != f_declared[1][i].type_:
                        print(f"Error: Type mismatch in {node.name} definition, expected {f_declared[1][i].type_.text} but got {p.type_.text}" )
                        print(f"line {node.line}: {node.text}")
                        sys.exit(1)
                    
                    if type(p) != type(f_declared[1][i]):
                        print(f"Error: Type mismatch in {node.name}, expected {type(f_declared[1][i])} but got {type(p)}" )
                        print(f"line {node.line}: {node.text}")
                        sys.exit(1)

            ctx.enter_block()

            # inject params into the context, with according types and flag can_define
            for p in params:
                ctx.set_type(p.name,p.type_, isinstance(p, VarParam))

            # If the func has a return, inject var with name of the func for the return
            if type_:
                ctx.set_type(name, type_)

            ctx.enter_block()
            # allow recursion
            ctx.add_function(f_context, False)
            for statement in block:
                type_check(ctx, statement)
            ctx.exit_block()
            ctx.exit_block()

            ctx.add_function(f_context, False)

        case Id(_,_,_,_,_,_,name):
            res = ctx.get_type(name)[0]
            node.type_ = res
            return res
        case IntLit(_,_,_,_,_,value):
            return IntType()
        case BooleanLit(_,_,_,_,_,value):
            return BooleanType()
        case FloatLit(_,_,_,_,_,value):
            return FloatType()
        case CharLit(_,_,_,_,_,value):
            return CharType()
        case String(_,_,_,_,_,value):
            return StringType()
        case _:
            raise TypeError(f"Unknown node type {node}")

def show_mismatch_error(node,type_, expr, msg):
    print(msg)
    print(f"line {node.line}: {node.text}")
    type_underline = f"{'^'*(type_.end_column - type_.column)}"
    type_space = ' ' * (len(f"line {node.line}: ") + type_.column - node.column)
    expr_underline = f"{'^'*(expr.end_column - expr.column)}"
    expr_space = ' ' * ( expr.column - type_.end_column)
    print(f"{type_space}{type_underline}{expr_space}{expr_underline}")
    sys.exit(1)

def show_simple_error(node, msg):
    print(msg)
    underline = f"{'^'*(node.end_column - node.column)}"
    print(f"line {node.line}: {node.text}")
    space = ' ' * (len(f"line {node.line}: "))
    print(f"{space}{underline}")
    sys.exit(1)


def type_check_program(filename):
    file = open(filename,"r")
    program = file.read()
    program_ast = parse_plush(program)
    typed_tree = type_check(Context(), program_ast)
    return typed_tree

if __name__ == "__main__":
    program = """
        val y: int := 1 + (1* true);
    """
    file = open("/home/alexandref/FCUL/compilers/plush_compiler/my_program.pl","r")
    program = file.read()
    # Example usage
    program_ast = parse_plush(program)
    # print(tree_to_string(program_ast))
    typed_tree = type_check(Context(), program_ast)
    for node in typed_tree.defs_or_decls:
        print(node.text)