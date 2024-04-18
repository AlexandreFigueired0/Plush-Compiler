from lark import Transformer, v_args
from ast_nodes import *

@v_args(inline=True)    # Affects the signatures of the methods
class PlushTree(Transformer):

    def start(self, *defs_or_decls):
        return Start(defs_or_decls)

    # DECLARATIONS

    def val_declaration(self, name, type_):
        return ValDeclaration(name, type_)
    
    def var_declaration(self, name, type_):
        return VarDeclaration(name, type_)
    
    def function_declaration(self, name, params, type_ = None):
        return FunctionDeclaration(name, params, type_)
    
    def params(self, *params):
        return list(params)
    
    def val_param(self, name, type_):
        return ValParam(name, type_)

    def var_param(self, name, type_):
        return VarParam(name, type_)
    
    # DEFINITIONS

    def val_definition(self, name, type_, expr):
        return ValDefinition(name, type_, expr)
    
    def var_definition(self, name, type_, expr):
        return VarDefinition(name, type_, expr)
    
    def function_definition(self, name, params, type_or_block, block= None):
        if isinstance(type_or_block, list):
            block = type_or_block
            type_ = None
        else:
            type_ = type_or_block

        return FunctionDefinition(name, params, type_, block)
    
    def assignment(self, name, expr):
        return Assignment(name, expr)
    
    def array_position_assignment(self, name, *index_and_expr):
        indexes = index_and_expr[:-1]
        expr = index_and_expr[-1]
        return ArrayPositionAssignment(name, indexes, expr)
    
    def block(self, *statements):
        return list(statements)

    # STATEMENTS

    def if_(self, condition, block):
        return If(condition, block)

    def if_else(self, condition, block, else_block):
        return IfElse(condition, block, else_block)
    
    def while_(self, condition, block):
        return While(condition, block)
    
    def concrete_params(self, *params):
        return list(params)

    def function_call(self, name, args):
        return FunctionCall(name, args)

    # TOKENS

    def NAME(self, token):
        return str(token)
    
    def INT(self, token):
        return str(token)
    
    def FLOAT(self, token):
        return str(token)
    
    def STRING(self, token):
        return str(token)
    
    def BOOLEAN(self, token):
        return str(token)
    
    # EXPRESSIONS
    def or_(self, left, right):
        return Or(left, right)
    
    def and_(self, left, right):
        return And(left, right)
    
    def equal(self, left, right):
        return Equal(left, right)
    
    def not_equal(self, left, right):
        return NotEqual(left, right)
    
    def lt(self, left, right):
        return LessThan(left, right)
    
    def gt(self, left, right):
        return GreaterThan(left, right)
    
    def lte(self, left, right):
        return LessThanOrEqual(left, right)
    
    def gte(self, left, right):
        return GreaterThanOrEqual(left, right)
    
    def add(self, left, right):
        return Add(left, right)
    
    def sub(self, left, right):
        return Sub(left, right)
    
    def power(self, left, right):
        return Power(left, right)
    
    def mul(self, left, right):
        return Mul(left, right)
    
    def div(self, left, right):
        return Div(left, right)
    
    def mod(self, left, right):
        return Mod(left, right)
    
    def unary_minus(self, expr):
        return UnaryMinus(expr)
    
    def not_(self, expr):
        return LogicNot(expr)
    
    def array_access(self, name, *indexes):
        return ArrayAccess(name, indexes)

    def id(self, name):
        return Id(name)

    def int_lit(self, value):
        return IntLit(value)
    
    def float_lit(self, value):
        return FloatLit(value)
    
    def boolean_lit(self, value):
        return BooleanLit(value)
    
    def string(self, value):
        return String(value)
    
    # TYPES

    def int_type(self):
        return IntType()
    
    def float_type(self):
        return FloatType()
    
    def double_type(self):
        return DoubleType()
    
    def string_type(self):
        return StringType()
    
    def char_type(self):
        return CharType()
    
    def boolean_type(self):
        return BooleanType()
    
    def array_type(self, type_):
        return ArrayType(type_)
    
def tree_to_string(tree, indent=0):
    tab = ' '*indent*4
    tab2 = ' '*indent*6
    match tree:
        case Start(defs_or_decls):
            return "start\n"+ "\n".join(map(lambda x : tree_to_string(x,indent+1), defs_or_decls))
        case ValDeclaration(name, type_):
            return f"{tab}val_decl\n{tab2}{name}\n{tab2}{type_}"
        case VarDeclaration(name, type_):
            return f"{tab}var_decl\n{tab2}{name}\n{tab2}{type_}"
        case FunctionDeclaration(name, params, type_):
            return f"{tab}func_decl\n{tab2}{name}\n{tab2}params\n" + "\n".join(map(lambda x : tree_to_string(x,indent+1), params)) + f"\n{tab2}{type_}"
        case ValParam(name, type_):
            return f"{tab}val_param\n{tab2}{name}\n{tab2}{type_}"
        case VarParam(name, type_):
            return f"{tab}var_param\n{tab2}{name}\n{tab2}{type_}"
        case ValDefinition(name, type_, expr):
            return f"{tab}val_def\n{tab2}{name}\n{tab2}{type_}\n{tree_to_string(expr,indent)}"
        case VarDefinition(name, type_, expr):
            return f"{tab}var_def\n{tab2}{name}\n{tab2}{type_}\n{tree_to_string(expr,indent)}"
        case Assignment(name, expr):
            return f"{tab}assign\n{tab2}{name}\n{tree_to_string(expr,indent)}"
        case FunctionDefinition(name, params, type_, block):
            return f"{tab}func_def\n{tab2}{name}\n{tab2}params\n" + "\n".join(map(lambda x : tree_to_string(x,indent+1), params)) +\
                f"\n{tab2}{type_}\n{tab2}block\n" + "\n".join(map(lambda x : tree_to_string(x,indent+1), block))
        
        #TODO: tab duvidoso
        case IntLit(value):
            return f"{tab2}int_lit{tab}{value}"