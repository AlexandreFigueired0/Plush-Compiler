
from ast_nodes import *
from tree_transformer import PlushTree
from plush_parser import parse_plush


class Context():
    def __init__(self):
        self.stack = [{}]
    
    def get_type(self, name):
        for scope in self.stack[::-1]:
            if name in scope:
                return scope[name]
        raise TypeError(f"Variable {name} doesn't exist")
    
    def set_type(self, name, value):
        scope = self.stack[0]
        scope[name] = value

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

def type_check(ctx : Context, node) -> bool:
    match node:
        case Start(defs_or_decls):
            for def_or_decl in defs_or_decls:
                type_check(ctx, def_or_decl)
        case ValDeclaration(name, type_) | VarDeclaration(name, type_):
            #TODO: Check if variable is already declared
            #TODO: Is this ok even if the prev ctx has this name
            if ctx.has_var_in_current_scope(name):
                raise TypeError(f"Variable {name} already declared")

            ctx.set_type(name, type_)
        case ValDefinition(name, type_, expr) | VarDefinition(name, type_, expr):

            # TODO: Check if variable is already declared
            if ctx.has_var_in_current_scope(name):
                raise TypeError(f"Variable {name} already declared")
            
            expr_type = type_check(ctx, expr)
            #TODO: floats can be assigned with ints?
            if type_ != expr_type :
                raise TypeError(f"Type mismatch for variable {name}, expected {type_} but got {expr_type}")
            ctx.set_type(name, type_)
        case Assignment(name, expr):
            #TODO: Check if variable is already declared
            if not ctx.has_var(name):
                raise TypeError(f"Variable {name} doesn't exist")
            
            var_type = ctx.get_type(name)
            expr_type = type_check(ctx, expr)
            if var_type != expr_type:
                raise TypeError(f"Type mismatch for variable {name}, expected {var_type} but got {expr_type}")
            
        case ArrayPositionAssignment(name, indexes, expr):
            if not ctx.has_var(name):
                raise TypeError(f"Variable {name} doesn't exist")
            
            var_type = ctx.get_type(name)

            
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
            #TODO: Como mostrar estes erros? eu nao sei se eh para ser float ou int
            if wrong_type not in [IntType(), FloatType()]:
                raise TypeError(f"Type mismatch in {node}, both operands must be both of type int or float but found {wrong_type}")

            if left_type != right_type:
                raise TypeError(f"Type mismatch in {node}, both operands must be both of type int or float but found {left_type} and {right_type}")

            return left_type
        
        case Or(left, right) | And(left, right) | Equal(left, right) | NotEqual(left, right) | GreaterThan(left, right) | \
              GreaterThanOrEqual(left, right) | LessThan(left, right) | LessThanOrEqual(left, right):
            
            left_type = type_check(ctx, left)
            right_type = type_check(ctx, right)

            wrong_type = left_type if left_type != BooleanType() else right_type
            if wrong_type != BooleanType():
                raise TypeError(f"Type mismatch in {node}, both operands must be of type boolean but found {wrong_type}")
            
            return BooleanType()
        
        case UnaryMinus(expr):
            expr_type = type_check(ctx, expr)
            if expr_type not in [IntType(), FloatType()]:
                raise TypeError(f"Type mismatch in {node}, operand must be a number but found {expr_type}")
            return expr_type
        
        case LogicNot(expr):
            expr_type = type_check(ctx, expr)
            if expr_type != BooleanType():
                raise TypeError(f"Type mismatch in {node}, operand must be of type boolean but found {expr_type}")
            return BooleanType()
        
        case ArrayAccess(name, indexes):
            if not ctx.has_var(name):
                raise TypeError(f"Variable {name} doesn't exist")
            
            var_type = ctx.get_type(name)
            
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
            return res_type

        case If(condition, block):
            condition_type = type_check(ctx, condition)
            if condition_type != BooleanType():
                raise TypeError(f"Type mismatch in {node}, condition must be of type boolean but found {condition_type}")
            
            #TODO: entr block?
            ctx.enter_block()
            type_check(ctx, block)
            ctx.exit_block()

        case IfElse(condition, block, else_block):
            condition_type = type_check(ctx, condition)
            if condition_type != BooleanType():
                raise TypeError(f"Type mismatch in {node}, condition must be of type boolean but found {condition_type}")
            
            #TODO: entr block?
            ctx.enter_block()
            type_check(ctx, block)
            ctx.exit_block()

            ctx.enter_block()
            type_check(ctx, else_block)
            ctx.exit_block()
        
        case While(condition, block):
            condition_type = type_check(ctx, condition)
            if condition_type != BooleanType():
                raise TypeError(f"Type mismatch in {node}, condition must be of type boolean but found {condition_type}")
            
            #TODO: entr block?
            ctx.enter_block()
            type_check(ctx, block)
            ctx.exit_block()
        
        #TODO: Check if the function exists
        #TODO: Check if the arguments are correct
        #TODO: Check if the return type is correct
        case FunctionCall(name, given_args):
            if not ctx.has_var(name):
                raise TypeError(f"Function {name} doesn't exist")
            
            f_context = ctx.get_type(name)

            #TODO: Check if this name is a function
            if not isinstance(f_context, tuple):
                raise TypeError(f"Function {name} is not callable")
            
            name, params, type_ = f_context
            # TODO: Check if the number of arguments is correct
            if len(params) != len(given_args):
                raise TypeError(f"Function {name} expects {len(params)} arguments but got {len(given_args)}")
            
            for i, arg in enumerate(given_args):
                arg_type = type_check(ctx, arg)
                if arg_type != params[i][1]:
                    raise TypeError(f"Type mismatch in {node}, expected {f_context[1][i][1]} but got {arg_type}")
            
            return f_context[2]

        case FunctionDeclaration(name, params, type_):
            if ctx.has_var(name):
                raise TypeError(f"Function {name} already declared")
            
            f_context = (name,[],type_)
            for p in params:
                f_context[1].append((p.name,p.type_))
            ctx.set_type(name, f_context)

        case FunctionDefinition(name, params, type_, block):
            f_context = (name,[],type_)

            ctx.enter_block()
            for p in params:
                ctx.set_type(p.name,p.type_)
                f_context[1].append((p.name,p.type_))

            # TODO: Check if the return type is correct
            ctx.set_type(name, type_)

            for statement in block:
                type_check(ctx, statement)
            ctx.exit_block()

            ctx.set_type(name, f_context)

        case Id(name):
            return ctx.get_type(name)
        case IntLit(value):
            return IntType()
        case BooleanLit(value):
            return BooleanType()
        case FloatLit(value):
            return FloatType()
        case String(value):
            return StringType()
        case _:
            raise TypeError(f"Unknown node type {node}")


if __name__ == "__main__":
    program = """
        val y: int := 1 + (1* true);
    """
    file = open("my_program.pl","r")
    program = file.read()
    # Example usage
    program_ast = parse_plush(program)
    # print(program_ast.pretty())
    type_check(Context(), program_ast)