from type_checker import type_check_program
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
    
    def set_val(self, name, value):
        scope = self.stack[-1]
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
            condition_val = interpret(ctx, condition)

            if  condition_val:
                ctx.enter_block()
                for statement in block:
                    interpret(ctx, statement)
                ctx.exit_block()

        case IfElse(condition, block, else_block):
            condition_val = interpret(ctx, condition)
            
            if condition_val:
                ctx.enter_block()
                for statement in block:
                    interpret(ctx, statement)
                ctx.exit_block()
            else:
                ctx.enter_block()
                for statement in else_block:
                    interpret(ctx, statement)
                ctx.exit_block()
        
        case While(condition, block):
            condition_val = interpret(ctx, condition)
            
            #TODO: entr block?
            ctx.enter_block()
            for statement in block:
                interpret(ctx, statement)
            ctx.exit_block()
        
        #TODO: Check if the function exists
        #TODO: Check if the arguments are correct
        #TODO: Check if the return type is correct
        case FunctionCall(name, given_args):
            if name == "print":
                str_to_print = interpret(ctx, given_args[0])
                print(str_to_print)
            elif name == "print_int":
                int_to_print = interpret(ctx, given_args[0])
                print(int_to_print)

        case FunctionDeclaration(name, params, type_):
            pass
        case FunctionDefinition(name, params, type_, block):
            if name == "main":
                for statement in block:
                    interpret(ctx, statement)
            else:
                raise NotImplementedError("FunctionDefinition")
        case Id(name):
            return ctx.get_val(name)
        case IntLit(value) | FloatLit(value) |  BooleanLit(value) :
            return value
        case CharLit(value) | String(value) :
            return value[1:-1] # remove quotes
        case _:
            raise TypeError(f"Unknown node type {node}")


filename = "my_program.pl"
typed_tree = type_check_program(filename)
interpret(Context(), typed_tree)