
from ast_nodes import *
from tree_transformer import PlushTree, tree_to_string
from plush_parser import parse_plush


class Context():
    def __init__(self):
        self.stack = [{}]
    
    def get_type(self, name):
        for scope in self.stack[::-1]:
            if name in scope:
                return scope[name]
        raise TypeError(f"Variable {name} doesn't exist")
    
    def set_type(self, name, value, can_define=True):
        scope = self.stack[-1]
        scope[name] = (value, can_define)

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
    ctx.set_type("print_int", ("print_int",[ValParam(name="x", type_ = IntType())],None), False)
    ctx.set_type("print_float", ("print_float",[ValParam(name="x", type_ = FloatType())],None), False)
    ctx.set_type("print_string", ("print_string",[ValParam(name="s", type_ = StringType())],None), False)
    ctx.set_type("power_int", ("power_int",[ValParam(name="b", type_ = IntType()), ValParam(name="e", type_ = IntType())],None), False)
    ctx.set_type("get_int_array", ("get_int_array",[ValParam(name="size", type_ = IntType())],ArrayType(type_=IntType())), False)

def gather_global_vars_and_funcs(ctx: Context, node):
    for global_node in node.defs_or_decls:
        match global_node:
            # case VarDefinition(vname, type_, expr):
            #     ctx.set_type(vname, type_)
            # case ValDefinition(vname, type_, expr):
            #     ctx.set_type(vname, type_, False)
            case FunctionDeclaration(name, params, type_):
                if ctx.has_var(name):
                    raise TypeError(f"Function {name} already declared")
                
                ctx.set_type(name, (name,params,type_))

            case FunctionDefinition(name, params, type_, block):
                if ctx.has_var(name) and ctx.get_type(name)[1] == False:
                    raise TypeError(f"Function {name} already defined")
                
                ctx.set_type(name, (name,params,type_), False)
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
        case ValDefinition(name, type_, expr) | VarDefinition(name, type_, expr):

            # TODO: Check if variable is already declared
            if ctx.has_var_in_current_scope(name):
                raise TypeError(f"Variable {name} already declared")
            
            expr_type = type_check(ctx, expr)
            #TODO: floats can be assigned with ints?
            if type_ != expr_type :
                raise TypeError(f"Type mismatch for variable {name}, expected {type_} but got {expr_type}")
            
            # If its a val, then cant be redefined
            ctx.set_type(name, type_, not isinstance(node, ValDefinition))
        case Assignment(name, expr):
            #TODO: Check if variable is already declared
            if not ctx.has_var(name):
                raise TypeError(f"Variable {name} doesn't exist")
            
            var_type,can_define = ctx.get_type(name)

            if not can_define:
                raise TypeError(f"Variable {name} is immutable")

            expr_type = type_check(ctx, expr)
            if var_type != expr_type:
                raise TypeError(f"Type mismatch for variable {name}, expected {var_type} but got {expr_type}")
            
        case ArrayPositionAssignment(name, indexes, expr):
            if not ctx.has_var(name):
                raise TypeError(f"Variable {name} doesn't exist")
            
            var_type, _ = ctx.get_type(name)

            
            #TODO: Check if the indexes are valid and go deeper in the type
            res_type = var_type
            for index in indexes:
                index_type = type_check(ctx, index)
                if index_type != IntType():
                    raise TypeError(f"Type mismatch in {node}, index must be of type int but found {index_type}")
                
                if not isinstance(res_type, ArrayType):
                    raise TypeError(f"Type mismatch in {node}, expected array but got {res_type}")

                res_type = res_type.type_
            
            expr_type = type_check(ctx, expr)
            if res_type != expr_type:
                raise TypeError(f"Type mismatch in {node}, expected {res_type} but got {expr_type}")

        case Sub(left, right) | Mul(left, right) | Div(left, right) | Mod(left, right) | Power(left, right) | \
                Add(left, right):
        
            left_type = type_check(ctx, left)
            right_type = type_check(ctx, right)

            wrong_type = left_type if left_type not in [IntType(), FloatType()] else right_type
            if wrong_type not in [IntType(), FloatType()]:
                raise TypeError(f"Type mismatch in {node}, both operands must be both of numerical type but found {wrong_type}")

            if left_type != right_type:
                raise TypeError(f"Type mismatch in {node}, both operands must be both of the same type but found {left_type} and {right_type}")

            node.type_ = left_type
            return left_type
        
        case Or(left, right) | And(left, right):
            
            left_type = type_check(ctx, left)
            right_type = type_check(ctx, right)

            wrong_type = left_type if left_type != BooleanType() else right_type
            if wrong_type != BooleanType():
                raise TypeError(f"Type mismatch in {node}, both operands must be of type boolean but found {wrong_type}")
            
            return BooleanType()
        
        case Equal(left, right) | NotEqual(left, right):
            
            left_type = type_check(ctx, left)
            right_type = type_check(ctx, right)

            if left_type != right_type:
                raise TypeError(f"Type mismatch in {node}, both operands must be of the same type but found {left_type} and {right_type}")
            
            return BooleanType()
        
        case GreaterThan(left, right) | GreaterThanOrEqual(left, right) | \
            LessThan(left, right) | LessThanOrEqual(left, right):

            left_type = type_check(ctx, left)
            right_type = type_check(ctx, right)

            wrong_type = left_type if left_type not in [IntType(), FloatType()] else right_type
            if wrong_type not in [IntType(), FloatType()]:
                raise TypeError(f"Type mismatch in {node}, both operands must be both of numerical type but found {wrong_type}")
            
            if left_type != right_type:
                raise TypeError(f"Type mismatch in {node}, both operands must be both of the same type but found {left_type} and {right_type}")
            
            return BooleanType()

        case UnaryMinus(expr):
            expr_type = type_check(ctx, expr)
            if expr_type not in [IntType(), FloatType()]:
                raise TypeError(f"Type mismatch in {node}, operand must be a number but found {expr_type}")
            
            node.type_ = expr_type
            return expr_type
        
        case LogicNot(expr):
            expr_type = type_check(ctx, expr)
            if expr_type != BooleanType():
                raise TypeError(f"Type mismatch in {node}, operand must be of type boolean but found {expr_type}")
            return BooleanType()
        
        case ArrayAccess(name, indexes):
            if not ctx.has_var(name):
                raise TypeError(f"Variable {name} doesn't exist")
            
            var_type,_ = ctx.get_type(name)

            #TODO: check if its a variable or a function call
            if isinstance(var_type, tuple):
                var_type = var_type[-1]
            
            #TODO: Check if the indexes are valid and go deeper in the type
            res_type = var_type
            for index in indexes:
                index_type = type_check(ctx, index)
                if index_type != IntType():
                    raise TypeError(f"Type mismatch in {node}, index must be of type int but found {index_type}")
                
                if not isinstance(res_type, ArrayType):
                    raise TypeError(f"Type mismatch in {node}, expected array but got {res_type}")
                res_type = res_type.type_
            
            # TODO: Access array, so return the type of the elem accessed
            node.type_ = res_type
            return res_type

        case If(condition, block):
            condition_type = type_check(ctx, condition)
            if condition_type != BooleanType():
                raise TypeError(f"Type mismatch in {node}, condition must be of type boolean but found {condition_type}")
            
            #TODO: entr block?
            ctx.enter_block()
            for statement in block:
                type_check(ctx, statement)
            ctx.exit_block()

        case IfElse(condition, block, else_block):
            condition_type = type_check(ctx, condition)
            if condition_type != BooleanType():
                raise TypeError(f"Type mismatch in {node}, condition must be of type boolean but found {condition_type}")
            
            #TODO: entr block?
            ctx.enter_block()
            for statement in block:
                type_check(ctx, statement)
            ctx.exit_block()

            ctx.enter_block()
            for statement in else_block:
                type_check(ctx, statement)
            ctx.exit_block()
        
        case While(condition, block):
            condition_type = type_check(ctx, condition)
            if condition_type != BooleanType():
                raise TypeError(f"Type mismatch in {node}, condition must be of type boolean but found {condition_type}")
            
            #TODO: entr block?
            ctx.enter_block()
            for statement in block:
                type_check(ctx, statement)
            ctx.exit_block()
        
        #TODO: Check if the function exists
        #TODO: Check if the arguments are correct
        #TODO: Check if the return type is correct
        case FunctionCall(name, given_args):
            if not ctx.has_var(name):
                raise TypeError(f"Function {name} doesn't exist")
            
            f_context,_ = ctx.get_type(name)

            #TODO: Check if this name is a function
            if not isinstance(f_context, tuple):
                raise TypeError(f"Function {name} is not callable")
            
            name, params, type_ = f_context
            # TODO: Check if the number of arguments is correct
            if len(params) != len(given_args):
                raise TypeError(f"Function {name} expects {len(params)} arguments but got {len(given_args)}")
            
            for i, arg in enumerate(given_args):
                arg_type = type_check(ctx, arg)
                if arg_type != params[i].type_:
                    raise TypeError(f"Type mismatch in {node}, expected {f_context[1][i].type_} but got {arg_type}")
            node.type_ = f_context[2]
            return f_context[2]

        case FunctionDeclaration(name, params, type_):

            
            f_context = (name,[],type_)
            for p in params:
                f_context[1].append(p)
            ctx.set_type(name, f_context)

        case FunctionDefinition(name, params, type_, block):
            f_context = (name,params,type_)


            # Function declared, but not defined
            # TODO: Check if the arguments are correct, type and immut modifiers
            if ctx.has_var(name) and ctx.get_type(name)[1] == True:
                f_declared,_ = ctx.get_type(name)

                if len(f_declared[1]) != len(params):
                    raise TypeError(f"Function {name} expects {len(f_declared[1])} arguments but got {len(params)}")
                
                for i, p in enumerate(params):
                    if p.type_ != f_declared[1][i].type_:
                        raise TypeError(f"Type mismatch in {node}, expected {f_declared[1][i].type_} but got {p.type_}")
                    
                    if type(p) != type(f_declared[1][i]):
                        raise TypeError(f"Type mismatch in {node}, expected {type(f_declared[1][i])} but got {type(p)}")

            ctx.enter_block()

            # TODO: inject params into the context, with according types and flag can_define
            for p in params:
                ctx.set_type(p.name,p.type_, isinstance(p, VarParam))

            # TODO: If the func has a return, inject var with name of the func for the return
            if type_:
                ctx.set_type(name, type_)

            for statement in block:
                type_check(ctx, statement)
            ctx.exit_block()

            ctx.set_type(name, f_context, False)

        case Id(name):
            res = ctx.get_type(name)[0]
            node.type_ = res
            return res
        case IntLit(value):
            return IntType()
        case BooleanLit(value):
            return BooleanType()
        case FloatLit(value):
            return FloatType()
        case CharLit(value):
            return CharType()
        case String(value):
            return StringType()
        case _:
            raise TypeError(f"Unknown node type {node}")


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
    file = open("my_program.pl","r")
    program = file.read()
    # Example usage
    program_ast = parse_plush(program)
    # print(tree_to_string(program_ast))
    typed_tree = type_check(Context(), program_ast)
    for node in typed_tree.defs_or_decls:
        print(node)