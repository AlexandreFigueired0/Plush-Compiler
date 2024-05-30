from lark import Lark, LarkError
from tree_transformer import PlushTree
import sys



plush_grammar = f"""
    start: (function_declaration | val_definition | var_definition | function_definition)*

    !?function_declaration: FUNCTION NAME "(" params ")" (":" type)? SEMICOLON -> function_declaration
    !?function_definition: FUNCTION NAME "(" params ")" (":" type)? block -> function_definition
    
    ?definition : val_definition
                | var_definition
                | assignment
                | array_position_assignment
    
    !?assignment  : NAME ":=" expression SEMICOLON -> assignment
    ?array_position_assignment: NAME ("[" expression "]")+ ":=" expression SEMICOLON

    !?val_definition  : VAL NAME ":" type ":=" expression SEMICOLON
    !?var_definition  : VAR NAME ":" type  ":=" expression SEMICOLON
    
    !params: param ("," param)*
            |
    !param  : VAL NAME ":" type  -> val_param
            | VAR NAME ":" type  -> var_param

    !block: LBRACE ( val_definition | var_definition | assignment | array_position_assignment | statement | (function_call ";") )* RBRACE

    !?statement  : IF  expression block -> if_
                | IF  expression block "else" block -> if_else
                | WHILE expression block -> while_
                
    
    ?expression  : logic_less_priority

    ?logic_less_priority : logic_high_priority
                        | logic_less_priority "||" logic_high_priority -> or_
    
    ?logic_high_priority : clause
                        | logic_high_priority "&&" clause -> and_
    
    ?clause  : arith_less_priority
            | arith_less_priority "=" arith_less_priority -> equal
            | arith_less_priority "!=" arith_less_priority -> not_equal
            | arith_less_priority "<" arith_less_priority -> lt
            | arith_less_priority ">" arith_less_priority -> gt
            | arith_less_priority "<=" arith_less_priority -> lte
            | arith_less_priority ">=" arith_less_priority -> gte
    
    ?arith_less_priority : arith_high_priority
                        | arith_less_priority "+" arith_high_priority   -> add
                        | arith_less_priority "-" arith_high_priority   -> sub

    ?arith_high_priority : atom
                        | arith_high_priority "^" arith_high_priority -> power
                        | arith_high_priority "*" atom  -> mul
                        | arith_high_priority "/" atom  -> div
                        | arith_high_priority "%" atom  -> mod
    
    ?atom    : INT       -> int_lit
            | FLOAT     -> float_lit
            | BOOLEAN   -> boolean_lit
            | NAME      -> id
            | STRING    -> string  
            | CHAR      -> char_lit
            | "-" atom -> unary_minus
            | "!" atom -> not_
            | "(" logic_less_priority ")"     
            | array_access 
            | function_call

    !function_call: NAME LPAREN concrete_params RPAREN
    ?array_access: (NAME|function_call) ("[" expression "]")+
    concrete_params: expression ("," expression)*  
                    |
    
    type: INT_TYPE -> int_type
        | FLOAT_TYPE -> float_type
        | STRING_TYPE -> string_type
        | CHAR_TYPE -> char_type
        | BOOLEAN_TYPE -> boolean_type
        | LSQUARE type RSQUARE -> array_type
    

    FUNCTION.4: /function\s+/
    VAL.4: /val\s+/
    VAR.4: /var\s+/
    IF.4: "if"
    WHILE.4: "while"

    SEMICOLON: ";"
    LSQUARE: "["
    RSQUARE: "]"
    LBRACE: "{{"
    RBRACE: "}}"
    LPAREN: "("
    RPAREN: ")"
    WHITESPACE: /[ \s]+/

    INT_TYPE: "int"
    FLOAT_TYPE: "float"
    STRING_TYPE: "string"
    CHAR_TYPE: "char"
    BOOLEAN_TYPE: "boolean"

    INT.1: /[0-9](_*[0-9])*/
    FLOAT.2: /[0-9]*\.[0-9]+/
    BOOLEAN.3: /true|false/
    STRING: /\"[^"]*\"/
    CHAR: /\'[^']\'/
    NAME.1: /[a-zA-Z_][a-zA-Z0-9_]*/

    COMMENT: /\#[^\n]+/x

    %import common.NEWLINE
    %import common.WS_INLINE

    %ignore WS_INLINE
    %ignore COMMENT
    %ignore NEWLINE

"""


parser = Lark(plush_grammar,parser="lalr", transformer=PlushTree())
# parser = Lark(plush_grammar,parser="lalr")




def parse_plush(program : str):
    try:
        return parser.parse(program.strip())
    except LarkError as e:
        line = e.line
        column = e.column
        column_end = column + len(e.token)
        print(f"Unknow token ({e.token}) at line {line}, column {column} to {column_end} in program") 
        sys.exit(1)



if __name__ == "__main__":
    # Example usage:
    program = """
        val x : int;
    """

    file = open("my_program.pl","r")
    program = file.read()
    tree = parse_plush(program)
    # print(tree.pretty())
    for node in tree.defs_or_decls:
        print(node.text)