from lark import Transformer, v_args, Token
from ast_nodes import *

@v_args(inline=True)    # Affects the signatures of the methods
class PlushTree(Transformer):

    def start(self, *defs_or_decls):
        return Start(defs_or_decls)

    # DECLARATIONS

    def function_declaration(self, fucntion_tok : Token, name : Token, params: list, type_or_sc : Type|Token, semicolon_tok : Token = None):
        if isinstance(type_or_sc, Type):
            type_ = type_or_sc
        else:
            type_ = None
            semicolon_tok = type_or_sc
        return FunctionDeclaration(name = name.value, params = params, type_ = type_,
        line_start=fucntion_tok.line, column_start=fucntion_tok.column, line_end=semicolon_tok.end_line, column_end=semicolon_tok.end_column)
    
    def params(self, *params):
        return list(params)
    
    def val_param(self, val_tok : Token,name : Token, type_ : Type):
        return ValParam(name = name.value, type_ = type_,
        line_start=val_tok.line, column_start=val_tok.column, line_end=type_.line_end, column_end=type_.column_end)

    def var_param(self, var_tok: Token, name : Token, type_ : Type):
        return VarParam(name = name, type_ = type_,
        line_start=var_tok.line, column_start=var_tok.column, line_end=type_.line_end, column_end=type_.column_end)
    
    # DEFINITIONS

    def val_definition(self,val_tok : Token, name : Token, type_ : Type, expr : Expression, semicolon_tok : Token):
        return ValDefinition(name = name.value, type_ = type_, expr = expr,
        line_start=val_tok.line, column_start=val_tok.column, line_end=semicolon_tok.end_line, column_end=semicolon_tok.end_column)
    
    def var_definition(self,var_tok : Token, name : Token, type_ : Type, expr : Expression, semicolon_tok : Token):
        return VarDefinition(name = name.value, type_ = type_, expr = expr,
        line_start=var_tok.line, column_start=var_tok.column, line_end=semicolon_tok.end_line, column_end=semicolon_tok.end_column)
    
    def function_definition(self, function_tok : Token, name : Token, params : list, type_or_block : Type|list, block : list= None):
        if isinstance(type_or_block, list):
            block = type_or_block
            type_ = None
        else:
            type_ = type_or_block

        rbracket_tok : Token = block[-1]
        block = block[1:-1]
        return FunctionDefinition(name = name.value, params = params, type_ = type_, block = block,
        line_start=function_tok.line, column_start=function_tok.column, line_end=rbracket_tok.end_line, column_end=rbracket_tok.end_column)
    
    def assignment(self, name : Token, expr : Expression, semicolon_tok : Token):
        return Assignment(name = name.value, expr = expr,
        line_start=name.line, column_start=name.column, line_end=semicolon_tok.end_line, column_end=semicolon_tok.end_line)
    
    def array_position_assignment(self, name : Token, *index_and_expr_and_sc : list):
        indexes:list = index_and_expr_and_sc[:-2]
        expr : Expression = index_and_expr_and_sc[-2]
        semicolon_tok : Token= index_and_expr_and_sc[-1]
        return ArrayPositionAssignment(name = name.value, indexes = indexes, expr = expr,
        line_start=name.line, column_start=name.column, line_end=semicolon_tok.end_line, column_end=semicolon_tok.end_column)
    
    def block(self, *statements):
        return list(statements)

    # STATEMENTS

    def if_(self, if_tok : Token, condition : Expression, block: list):

        rbracket_tok : Token = block[-1]
        block = block[1:-1]
        return If(condition=condition, block=block,
        line_start=if_tok.line, column_start=if_tok.column, line_end=rbracket_tok.end_line, column_end=rbracket_tok.end_column)

    def if_else(self, if_tok : Token, condition: Expression, block: list, else_block: list):
        
        last_rsqure_tok = else_block[-1]
        block = block[1:-1]
        else_block = else_block[1:-1]
        return IfElse(condition=condition, block =block, else_block=else_block,
        line_start=if_tok.line, column_start=if_tok.column, line_end=last_rsqure_tok.end_line, column_end=last_rsqure_tok.end_column)
    
    def while_(self, while_tok : Token, condition :Expression, block: list):
        rbracket_tok : Token = block[-1]
        block = block[1:-1]
        return While(condition=condition, block =block,
        line_start=while_tok.line, column_start=while_tok.column, line_end=rbracket_tok.end_line, column_end=rbracket_tok.end_column)
    
    def concrete_params(self, *params):
        return list(params)

    def function_call(self, name : Token, lparen_tok : Token ,args : list[Expression], rparen_tok : Token):
        return FunctionCall(name = name.value, args =  args , type_=None,
        line_start=name.line, column_start=name.column, line_end=rparen_tok.end_line, column_end=rparen_tok.end_column)

    
    # EXPRESSIONS
    def or_(self, left : Expression, right : Expression):
        return Or(left = left, right = right, type_=BooleanType(line_start=0, column_start=0, line_end=0, column_end=0),
        line_start=left.line_start, column_start=left.column_start, line_end=right.line_end, column_end=right.column_end)
    
    def and_(self, left : Expression, right : Expression):
        return And(left = left, right = right, type_=BooleanType(line_start=0, column_start=0, line_end=0, column_end=0),
        line_start=left.line_start, column_start=left.column_start, line_end=right.line_end, column_end=right.column_end)
    
    def equal(self, left : Expression, right : Expression):
        return Equal(left = left, right = right, type_=BooleanType(line_start=0, column_start=0, line_end=0, column_end=0),
        line_start=left.line_start, column_start=left.column_start, line_end=right.line_end, column_end=right.column_end)
    
    def not_equal(self, left : Expression, right : Expression):
        return NotEqual(left = left, right = right, type_=BooleanType(line_start=0, column_start=0, line_end=0, column_end=0),
        line_start=left.line_start, column_start=left.column_start, line_end=right.line_end, column_end=right.column_end)
    
    def lt(self, left : Expression, right : Expression):
        return LessThan(left = left, right = right, type_=BooleanType(line_start=0, column_start=0, line_end=0, column_end=0),
        line_start=left.line_start, column_start=left.column_start, line_end=right.line_end, column_end=right.column_end)
    
    def gt(self, left : Expression, right : Expression):
        return GreaterThan(left = left, right = right, type_=BooleanType(line_start=0, column_start=0, line_end=0, column_end=0),
        line_start=left.line_start, column_start=left.column_start, line_end=right.line_end, column_end=right.column_end)
    
    def lte(self, left : Expression, right : Expression):
        return LessThanOrEqual(left = left, right = right, type_=BooleanType(line_start=0, column_start=0, line_end=0, column_end=0),
        line_start=left.line_start, column_start=left.column_start, line_end=right.line_end, column_end=right.column_end)
    
    def gte(self, left : Expression, right : Expression):
        return GreaterThanOrEqual(left = left, right = right, type_=BooleanType(line_start=0, column_start=0, line_end=0, column_end=0),
        line_start=left.line_start, column_start=left.column_start, line_end=right.line_end, column_end=right.column_end)
    
    def add(self, left : Expression, right : Expression):
        return Add(left = left, right = right, type_=None,
        line_start=left.line_start, column_start=left.column_start, line_end=right.line_end, column_end=right.column_end)
    
    def sub(self, left : Expression, right : Expression):
        return Sub(left = left, right = right, type_=None,
        line_start=left.line_start, column_start=left.column_start, line_end=right.line_end, column_end=right.column_end)
    
    def power(self, left : Expression, right : Expression):
        return Power(left = left, right = right, type_=None,
        line_start=left.line_start, column_start=left.column_start, line_end=right.line_end, column_end=right.column_end)
    
    def mul(self, left : Expression, right : Expression):
        return Mul(left = left, right = right, type_=None,
        line_start=left.line_start, column_start=left.column_start, line_end=right.line_end, column_end=right.column_end)
    
    def div(self, left : Expression, right : Expression):
        return Div(left = left, right = right, type_=None,
        line_start=left.line_start, column_start=left.column_start, line_end=right.line_end, column_end=right.column_end)
    
    def mod(self, left : Expression, right : Expression):
        return Mod(left = left, right = right, type_=IntType(line_start=0, column_start=0, line_end=0, column_end=0),
        line_start=left.line_start, column_start=left.column_start, line_end=right.line_end, column_end=right.column_end)
    
    def unary_minus(self, expr : Expression):
        return UnaryMinus(expr = expr, type_=None,
        line_start=expr.line_start, column_start=expr.column_start, line_end=expr.line_end, column_end=expr.column_end)
    
    def not_(self, expr : Expression):
        return LogicNot(expr = expr, type_=None,
        line_start=expr.line_start, column_start=expr.column_start, line_end=expr.line_end, column_end=expr.column_end)
    
    def array_access(self, name_or_fcall, *indexes: list[Expression]):
        if isinstance(name_or_fcall, FunctionCall):
            return FunctionCallArrayAccess(fcall =name_or_fcall, indexes=indexes, type_=None,
        line_start=name_or_fcall.line_start, column_start=name_or_fcall.column_start, line_end=indexes[-1].line_end, column_end=indexes[-1].column_end)
        return ArrayAccess(name = name_or_fcall, indexes = indexes, type_=None,
        line_start=name_or_fcall.line, column_start=name_or_fcall.column, line_end=indexes[-1].line_end, column_end=indexes[-1].column_end)

    def id(self, name : Token):
        return Id(name = name, type_=None,
        line_start=name.line, column_start=name.column, line_end=name.end_line, column_end=name.end_column)

    def int_lit(self, value : Token):
        return IntLit(value = value.value.replace("_", ""), type_=IntType(line_start=0, column_start=0, line_end=0, column_end=0),
        line_start=value.line, column_start=value.column, line_end=value.end_line, column_end=value.end_column)
    
    def float_lit(self, value : Token):
        return FloatLit(value = value.value, type_=FloatType(line_start=0, column_start=0, line_end=0, column_end=0),
        line_start=value.line, column_start=value.column, line_end=value.end_line, column_end=value.end_column)
    
    def boolean_lit(self, value : Token):
        return BooleanLit(value = value.value, type_=BooleanType(line_start=0, column_start=0, line_end=0, column_end=0),
        line_start=value.line, column_start=value.column, line_end=value.end_line, column_end=value.end_column)
    
    def char_lit(self, value : Token):
        return CharLit(value =value.value[1:-1], type_=CharType(line_start=0, column_start=0, line_end=0, column_end=0),
        line_start=value.line, column_start=value.column, line_end=value.end_line, column_end=value.end_column)
    
    def string(self, value : Token):
        return String(value =value.value[1:-1], type_=StringType(line_start=0, column_start=0, line_end=0, column_end=0),
        line_start=value.line, column_start=value.column, line_end=value.end_line, column_end=value.end_column)
    
    # TYPES

    def int_type(self, type_tok : Token):
        return IntType(line_start=type_tok.line, column_start=type_tok.column, line_end=type_tok.end_line, column_end=type_tok.end_column)
    
    def float_type(self, type_tok : Token):
        return FloatType(line_start=type_tok.line, column_start=type_tok.column, line_end=type_tok.end_line, column_end=type_tok.end_column)
    
    def string_type(self, type_tok : Token):
        return StringType(line_start=type_tok.line, column_start=type_tok.column, line_end=type_tok.end_line, column_end=type_tok.end_column)
    
    def char_type(self, type_tok : Token):
        return CharType(line_start=type_tok.line, column_start=type_tok.column, line_end=type_tok.end_line, column_end=type_tok.end_column)
    
    def boolean_type(self, type_tok : Token):
        return BooleanType(line_start=type_tok.line, column_start=type_tok.column, line_end=type_tok.end_line, column_end=type_tok.end_column)
    
    def array_type(self, lsquare_tok : Token, type_ : Type, rsquare_tok : Token):
        return ArrayType(type_=type_,
        line_start=lsquare_tok.line, column_start=lsquare_tok.column, line_end=rsquare_tok.end_line, column_end=rsquare_tok.end_column)
