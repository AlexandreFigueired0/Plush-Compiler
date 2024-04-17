from lark import Transformer, v_args
from ast_nodes import *

@v_args(inline=True)    # Affects the signatures of the methods
class PlushTree(Transformer):

    def start(self, *defs_or_decls):
        return list(defs_or_decls)

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
    
    def array_position_assignment(self, name, position, expr):
        return ArrayPositionAssignment(name, position, expr)
    
    def block(self, *statements):
        return list(statements)

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
    
    def boolean_type(self):
        return BooleanType()
    
    def array_type(self, type_):
        return ArrayType(type_)