from lark import Transformer, v_args, Token
import src.pl_parser.ast_nodes as ast
ws = " "

# Helper function to insert token text into the result list
def unparse(*tokens : list[Token|ast.Node]):
    """
    Builds the original string from the tokens
    """
    max_line = max(token.line for token in tokens)
    min_line = min(token.line for token in tokens)
    max_column = max(token.end_column for token in tokens)
    min_column = min(token.column for token in tokens)
    result = [[' '] * max_column for _ in range(max_line)]

    for token in tokens:
        line = token.line - min_line
        start = token.column - min_column
        end = token.end_column - min_column
        result[line][start:end] = list(token) if isinstance(token, Token) else list(token.text)

    # Join each line into a single string, then join all lines with line breaks
    return "\n".join("".join(line).replace("\n", "") for line in result).strip()


@v_args(inline=True)    # Affects the signatures of the methods
class PlushTree(Transformer):

    def start(self, *defs_or_decls):
        return ast.Start(defs_or_decls)
    
    # IMPORT
    def import_(self, from_tok, file : str, func_names : list):
        return ast.Import(file=file, func_names= func_names)
    
    def imported_functions(self, *names):
        return list(names)

    # DECLARATIONS

    def function_declaration(self, fucntion_tok : Token, name : Token, lparen_tok : Token,params: list, rparen_tok : Token, *type_sc : list):
        text = ""
        if type_sc[0] == ":":
            colon_tok = type_sc[0]
            type_ = type_sc[1]
            semicolon_tok = type_sc[2]
            text = unparse(fucntion_tok, name, lparen_tok, *params, rparen_tok,colon_tok, type_, semicolon_tok)
        else:
            type_ = None
            semicolon_tok = type_sc[0]
            text = unparse(fucntion_tok, name, lparen_tok, *params, rparen_tok, semicolon_tok)
        params = list(filter(lambda x: isinstance(x,(ast.ValParam,ast.VarParam)), params))
        return ast.FunctionDeclaration(name = name.value, params = params, type_ = type_,
        line=fucntion_tok.line, column=fucntion_tok.column, end_line=semicolon_tok.end_line, end_column=semicolon_tok.end_column, text=text)
    
    def params(self, *params):
        return list(params)
    
    def val_param(self, val_tok : Token,name : Token, colon_tok : Token, type_ : ast.Type):
        text = unparse(val_tok, name, colon_tok, type_)
        return ast.ValParam(name = name.value, type_ = type_,
        line=val_tok.line, column=val_tok.column, end_line=type_.end_line, end_column=type_.end_column, text=text)

    def var_param(self, var_tok: Token,name : Token, colon_tok : Token, type_ : ast.Type):
        text = unparse(var_tok, name, colon_tok, type_)
        return ast.VarParam(name = name.value, type_ = type_,
        line=var_tok.line, column=var_tok.column, end_line=type_.end_line, end_column=type_.end_column, text = text)
    
    # DEFINITIONS

    def val_definition(self,val_tok : Token, name : Token, colon_tok : Token, type_ : ast.Type, assign_tok : Token, expr : ast.Expression, semicolon_tok : Token):
        text = unparse(val_tok, name, colon_tok, type_, assign_tok, expr, semicolon_tok)

        return ast.ValDefinition(name = name.value, type_ = type_, expr = expr,
        line=val_tok.line, column=val_tok.column, end_line=semicolon_tok.end_line, end_column=semicolon_tok.end_column, text=text)
    
    def var_definition(self,var_tok : Token, name : Token, colon_tok : Token, type_ : ast.Type, assign_tok : Token, expr : ast.Expression, semicolon_tok : Token):
        text = unparse(var_tok, name, colon_tok, type_, assign_tok, expr, semicolon_tok)
        return ast.VarDefinition(name = name.value, type_ = type_, expr = expr,
        line=var_tok.line, column=var_tok.column, end_line=semicolon_tok.end_line, end_column=semicolon_tok.end_column, text=text)
    
    def function_definition(self, function_tok : Token, name : Token, lparen_tok:Token, params : list, rparen_tok : Token, *type_or_block: list):
        text = ""
        if isinstance(type_or_block[0], list):
            block = type_or_block[0]
            type_ = None
            text = unparse(function_tok, name, lparen_tok, *params, rparen_tok, *block)
        else:
            colon_tok = type_or_block[0]
            type_ = type_or_block[1]
            block = type_or_block[2]
            text = unparse(function_tok, name, lparen_tok, *params, rparen_tok, colon_tok, type_, *block)

        rbracket_tok : Token = block[-1]
        block = block[1:-1]
        params = list(filter(lambda x: isinstance(x,(ast.ValParam,ast.VarParam)), params))
        return ast.FunctionDefinition(name = name.value, params = params, type_ = type_, block = block,
        line=function_tok.line, column=function_tok.column, end_line=rbracket_tok.end_line, end_column=rbracket_tok.end_column, text=text)
    
    def assignment(self, name : Token, assign_tok : Token ,expr : ast.Expression, semicolon_tok : Token):
        text = unparse(name, assign_tok, expr, semicolon_tok)
        return ast.Assignment(name = name.value, expr = expr,
        line=name.line, column=name.column, end_line=semicolon_tok.end_line, end_column=semicolon_tok.end_column, text=text)
    
    def array_position_assignment(self, name : Token, *index_and_expr_and_sc : list):
        indexes:list = index_and_expr_and_sc[:-2]
        expr : ast.Expression = index_and_expr_and_sc[-2]
        semicolon_tok : Token= index_and_expr_and_sc[-1]
        indexes_text = "".join([f"[{index.text}]" for index in indexes])
        text = f"{name.value}{indexes_text}"
        return ast.ArrayPositionAssignment(name = name.value, indexes = indexes, expr = expr,
        line=name.line, column=name.column, end_line=semicolon_tok.end_line, end_column= name.column + len(indexes_text)+1, text=text)
    
    def block(self, *statements):
        return list(statements)

    # STATEMENTS

    def if_(self, if_tok : Token, condition : ast.Expression, block: list):

        rbracket_tok : Token = block[-1]
        block = block[1:-1]
        return ast.If(condition=condition, block=block,
        line=if_tok.line, column=if_tok.column, end_line=rbracket_tok.end_line, end_column=rbracket_tok.end_column)

    def if_else(self, if_tok : Token, condition: ast.Expression, block: list, else_tok:Token, else_block: list):
        
        last_rsqure_tok = else_block[-1]
        block = block[1:-1]
        else_block = else_block[1:-1]
        return ast.IfElse(condition=condition, block =block, else_block=else_block,
        line=if_tok.line, column=if_tok.column, end_line=last_rsqure_tok.end_line, end_column=last_rsqure_tok.end_column)
    
    def while_(self, while_tok : Token, condition :ast.Expression, block: list):
        rbracket_tok : Token = block[-1]
        block = block[1:-1]
        return ast.While(condition=condition, block =block,
        line=while_tok.line, column=while_tok.column, end_line=rbracket_tok.end_line, end_column=rbracket_tok.end_column)
    
    def concrete_params(self, *params):
        return list(params)

    def function_call(self, name : Token, lparen_tok : Token ,args : list[ast.Expression], rparen_tok : Token):
        text_args = []
        for a in args:
            text_args.append(a)
            text_args.append(Token("COMMA", ",", line=a.line, column=a.end_column, end_line=a.end_line, end_column=a.end_column+1))
        text = unparse(name, lparen_tok, *text_args, rparen_tok)
        return ast.FunctionCall(name = name.value, args =  args , type_=None,
        line=name.line, column=name.column, end_line=rparen_tok.end_line, end_column=rparen_tok.end_column, text=text)

    
    # EXPRESSIONS
    def or_(self, left : ast.Expression, or_tok : Token,right : ast.Expression):
        text = unparse(left, or_tok, right)
        return ast.Or(left = left, right = right, type_=ast.BooleanType(line=0, column=0, end_line=0, end_column=0),
        line=left.line, column=left.column, end_line=right.end_line, end_column=right.end_column, text=text)
    
    def and_(self, left : ast.Expression,and_tok : Token, right : ast.Expression):
        text = unparse(left, and_tok, right)
        return ast.And(left = left, right = right, type_=ast.BooleanType(line=0, column=0, end_line=0, end_column=0),
        line=left.line, column=left.column, end_line=right.end_line, end_column=right.end_column, text=text)
    
    def equal(self, left : ast.Expression, eq_tok : Token, right : ast.Expression):
        text = unparse(left, eq_tok, right)
        return ast.Equal(left = left, right = right, type_=ast.BooleanType(line=0, column=0, end_line=0, end_column=0),
        line=left.line, column=left.column, end_line=right.end_line, end_column=right.end_column, text=text)
    
    def not_equal(self, left : ast.Expression, neq_tok : Token, right : ast.Expression):
        text = unparse(left, neq_tok, right)
        return ast.NotEqual(left = left, right = right, type_=ast.BooleanType(line=0, column=0, end_line=0, end_column=0),
        line=left.line, column=left.column, end_line=right.end_line, end_column=right.end_column, text=text)
    
    def lt(self, left : ast.Expression, lt_tok: Token, right : ast.Expression):
        text = unparse(left, lt_tok, right)
        return ast.LessThan(left = left, right = right, type_=ast.BooleanType(line=0, column=0, end_line=0, end_column=0),
        line=left.line, column=left.column, end_line=right.end_line, end_column=right.end_column, text=text)
    
    def gt(self, left : ast.Expression, gt_tok: Token, right : ast.Expression):
        text = unparse(left, gt_tok, right)
        return ast.GreaterThan(left = left, right = right, type_=ast.BooleanType(line=0, column=0, end_line=0, end_column=0),
        line=left.line, column=left.column, end_line=right.end_line, end_column=right.end_column, text=text)
    
    def lte(self, left : ast.Expression, lte_tok : Token, right : ast.Expression):
        text = unparse(left, lte_tok, right)
        return ast.LessThanOrEqual(left = left, right = right, type_=ast.BooleanType(line=0, column=0, end_line=0, end_column=0),
        line=left.line, column=left.column, end_line=right.end_line, end_column=right.end_column, text=text)
    
    def gte(self, left : ast.Expression,gte_tok : Token, right : ast.Expression):
        text = unparse(left, gte_tok, right)
        return ast.GreaterThanOrEqual(left = left, right = right, type_=ast.BooleanType(line=0, column=0, end_line=0, end_column=0),
        line=left.line, column=left.column, end_line=right.end_line, end_column=right.end_column, text=text)
    
    def add(self, left : ast.Expression, add_tok : Token ,right : ast.Expression):
        text = unparse(left, add_tok, right)
        return ast.Add(left = left, right = right, type_=None,
        line=left.line, column=left.column, end_line=right.end_line, end_column=right.end_column, text=text)
    
    def sub(self, left : ast.Expression, sub_tok:Token, right : ast.Expression):
        text = unparse(left, sub_tok, right)
        return ast.Sub(left = left, right = right, type_=None,
        line=left.line, column=left.column, end_line=right.end_line, end_column=right.end_column, text=text)
    
    def power(self, left : ast.Expression,power_tok : Token, right : ast.Expression):
        text = unparse(left, power_tok, right)
        return ast.Power(left = left, right = right, type_=None,
        line=left.line, column=left.column, end_line=right.end_line, end_column=right.end_column, text=text)
    
    def mul(self, left : ast.Expression, muk_tok : Token, right : ast.Expression):
        text = unparse(left, muk_tok, right)
        return ast.Mul(left = left, right = right, type_=None,
        line=left.line, column=left.column, end_line=right.end_line, end_column=right.end_column, text=text)
    
    def div(self, left : ast.Expression, div_tok: Token, right : ast.Expression):
        text = unparse(left, div_tok, right)
        return ast.Div(left = left, right = right, type_=None,
        line=left.line, column=left.column, end_line=right.end_line, end_column=right.end_column, text=text)
    
    def mod(self, left : ast.Expression, mod_tok : Token, right : ast.Expression):
        text = unparse(left, mod_tok, right)
        return ast.Mod(left = left, right = right, type_=ast.IntType(line=0, column=0, end_line=0, end_column=0),
        line=left.line, column=left.column, end_line=right.end_line, end_column=right.end_column, text=text)
    
    def unary_minus(self, um_tok:Token, expr : ast.Expression):
        text = unparse(um_tok, expr)
        return ast.UnaryMinus(expr = expr, type_=None,
        line=expr.line, column=um_tok.column, end_line=expr.end_line, end_column=expr.end_column, text=text)
    
    def not_(self, not_tok:Token, expr : ast.Expression):
        text = unparse(not_tok, expr)
        return ast.LogicNot(expr = expr, type_=None,
        line=expr.line, column=not_tok.column, end_line=expr.end_line, end_column=expr.end_column, text=text)
    
    def array_access(self, name_or_fcall, *indexes: list[ast.Expression]):
        indexes_text = "".join([f"[{index.text}]" for index in indexes])
        if isinstance(name_or_fcall, ast.FunctionCall):
            text = f"{name_or_fcall.text}{indexes_text}"
            return ast.FunctionCallArrayAccess(fcall =name_or_fcall, indexes=indexes, type_=None,
        line=name_or_fcall.line, column=name_or_fcall.column, end_line=indexes[-1].end_line, end_column=name_or_fcall.column + len(text), text=text)

        text = f"{name_or_fcall.value}{indexes_text}"
        return ast.ArrayAccess(name = name_or_fcall.value, indexes = indexes, type_=None,
        line=name_or_fcall.line, column=name_or_fcall.column, end_line=indexes[-1].end_line, end_column=name_or_fcall.column + len(indexes_text)+1, text=text)

    def id(self, name : Token):
        return ast.Id(name = name.value, type_=None,
        line=name.line, column=name.column, end_line=name.end_line, end_column=name.end_column, text = name.value)

    def int_lit(self, value : Token):
        return ast.IntLit(value = value.value.replace("_", ""), type_=ast.IntType(line=0, column=0, end_line=0, end_column=0),
        line=value.line, column=value.column, end_line=value.end_line, end_column=value.end_column, text= value.value)
    
    def float_lit(self, value : Token):
        return ast.FloatLit(value = value.value, type_=ast.FloatType(line=0, column=0, end_line=0, end_column=0),
        line=value.line, column=value.column, end_line=value.end_line, end_column=value.end_column, text= value.value)
    
    def boolean_lit(self, value : Token):
        return ast.BooleanLit(value = value.value, type_=ast.BooleanType(line=0, column=0, end_line=0, end_column=0),
        line=value.line, column=value.column, end_line=value.end_line, end_column=value.end_column, text= value.value)
    
    def char_lit(self, value : Token):
        return ast.CharLit(value =value.value[1:-1], type_=ast.CharType(line=0, column=0, end_line=0, end_column=0),
        line=value.line, column=value.column, end_line=value.end_line, end_column=value.end_column, text= value.value)
    
    def string(self, value : Token):
        return ast.String(value =value.value[1:-1], type_=ast.StringType(line=0, column=0, end_line=0, end_column=0),
        line=value.line, column=value.column, end_line=value.end_line, end_column=value.end_column, text= value.value)
    
    # TYPES

    def int_type(self, type_tok : Token):
        return ast.IntType(line=type_tok.line, column=type_tok.column, end_line=type_tok.end_line, end_column=type_tok.end_column, text="int")
    
    def float_type(self, type_tok : Token):
        return ast.FloatType(line=type_tok.line, column=type_tok.column, end_line=type_tok.end_line, end_column=type_tok.end_column, text="float")
    
    def string_type(self, type_tok : Token):
        return ast.StringType(line=type_tok.line, column=type_tok.column, end_line=type_tok.end_line, end_column=type_tok.end_column, text="string")
    
    def char_type(self, type_tok : Token):
        return ast.CharType(line=type_tok.line, column=type_tok.column, end_line=type_tok.end_line, end_column=type_tok.end_column, text="char")
    
    def boolean_type(self, type_tok : Token):
        return ast.BooleanType(line=type_tok.line, column=type_tok.column, end_line=type_tok.end_line, end_column=type_tok.end_column, text="boolean")
    
    def array_type(self, lsquare_tok : Token, type_ : ast.Type, rsquare_tok : Token):
        return ast.ArrayType(type_=type_,
        line=lsquare_tok.line, column=lsquare_tok.column, end_line=rsquare_tok.end_line, end_column=rsquare_tok.end_column, text=f"[{type_.text}]")
