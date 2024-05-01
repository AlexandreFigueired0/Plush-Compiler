from type_checker import type_check
from ast_nodes import *
from tree_transformer import PlushTree, tree_to_string
from plush_parser import parse_plush

OPERATORS = {  
    Add: "+",
    Sub: "-",
    Mul: "*",
    Div: "/",
    Mod: "%",
    Power: "**",
    Equal: "==",
    NotEqual: "!=",
    GreaterThan: ">",
    GreaterThanOrEqual: ">=",
    LessThan: "<",
    LessThanOrEqual: "<=",
    And: "and",
    Or: "or",
    LogicNot: "not",
    UnaryMinus: "-",
}

class Context():
    def __init__(self):
        self.stack = [{}]
    
    def get_val(self, name):
        for scope in self.stack[::-1]:
            if name in scope:
                return scope[name]
        raise TypeError(f"Variable {name} doesn't exist")
    
    def set_val(self, name, value, can_define=True):
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

def interpret(ctx: Context, node):
    match node:
        case Start(defs_or_decls):
            for def_or_decl in defs_or_decls:
                interpret(ctx, def_or_decl)
        case ValDefinition(name, type_, expr) | VarDefinition(name, type_, expr):
            val = interpret(ctx, expr)
            ctx.set_val(name, val)
        case Assignment(name, expr):
            val = interpret(ctx, expr)
            ctx.set_val(name, val)
        case ArrayPositionAssignment(name, indexes, expr):
            raise NotImplementedError("ArrayPositionAssignment")
        
        case Sub(left, right) | Mul(left, right) | Div(left, right) | Mod(left, right) | Power(left, right) | \
                Add(left, right) | Or(left, right) | And(left, right) | Equal(left, right) | NotEqual(left, right) | \
                GreaterThan(left, right) | GreaterThanOrEqual(left, right) | LessThan(left, right) | LessThanOrEqual(left, right):
        
            left_val = interpret(ctx, left)
            right_val = interpret(ctx, right)
            op = OPERATORS[type(node)]
            return eval(f"{left_val} {op} {right_val}")
        
        case UnaryMinus(expr):
            expr_val = interpret(ctx, expr)
            return -expr_val
        
        case LogicNot(expr):
            expr_val = interpret(ctx, expr)
            return not expr_val
        
        case ArrayAccess(name, indexes):
            raise NotImplementedError("ArrayAccess")

        case If(condition, block):
            condition_type = interpret(ctx, condition)
            if condition_type != BooleanType():
                raise TypeError(f"Type mismatch in {node}, condition must be of type boolean but found {condition_type}")
            
            #TODO: entr block?
            ctx.enter_block()
            interpret(ctx, block)
            ctx.exit_block()

        case IfElse(condition, block, else_block):
            condition_type = interpret(ctx, condition)
            if condition_type != BooleanType():
                raise TypeError(f"Type mismatch in {node}, condition must be of type boolean but found {condition_type}")
            
            #TODO: entr block?
            ctx.enter_block()
            interpret(ctx, block)
            ctx.exit_block()

            ctx.enter_block()
            interpret(ctx, else_block)
            ctx.exit_block()
        
        case While(condition, block):
            condition_type = interpret(ctx, condition)
            if condition_type != BooleanType():
                raise TypeError(f"Type mismatch in {node}, condition must be of type boolean but found {condition_type}")
            
            #TODO: entr block?
            ctx.enter_block()
            interpret(ctx, block)
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
                arg_type = interpret(ctx, arg)
                if arg_type != params[i].type_:
                    raise TypeError(f"Type mismatch in {node}, expected {f_context[1][i][1]} but got {arg_type}")
            node.type_ = f_context[2]
            return f_context[2]

        case FunctionDeclaration(name, params, type_):
            if ctx.has_var(name):
                raise TypeError(f"Function {name} already declared")
            
            f_context = (name,[],type_)
            for p in params:
                f_context[1].append(p)
            ctx.set_type(name, f_context)

        case FunctionDefinition(name, params, type_, block):
            f_context = (name,params,type_)

            # Function already defined
            if ctx.has_var(name) and ctx.get_type(name)[1] == False:
                raise TypeError(f"Function {name} already defiend")
            # Function declared, but not defined
            # TODO: Check if the arguments are correct, type and modifiers
            elif ctx.has_var(name) and ctx.get_type(name)[1] == True:
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

            # TODO: Check if the return type is correct
            ctx.set_type(name, type_)

            for statement in block:
                interpret(ctx, statement)
            ctx.exit_block()

            ctx.set_type(name, f_context, False)

        case Id(name):
            return ctx.get_type(name)[0]
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


file = open("my_program.pl","r")
program = file.read()
# Example usage
program_ast = parse_plush(program)
# print(tree_to_string(program_ast))
typed_tree = type_check(Context(), program_ast)
interpret(Context(), typed_tree)