from lark import Lark, LarkError
from src.pl_parser.tree_transformer import PlushTree
from src.pl_parser.ast_nodes import *
import sys



plush_grammar = fr"""
    start: (function_declaration | val_definition | var_definition | function_definition | import_)*

    !?function_declaration: FUNCTION NAME "(" params ")" (":" type)? SEMICOLON -> function_declaration
    !?function_definition: FUNCTION NAME "(" params ")" (":" type)? block -> function_definition
    ?import_: FROM NAME "import" imported_functions
    imported_functions: (NAME ("," NAME)*) | STAR
    
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

    block: LBRACE ( val_definition | var_definition | assignment | array_position_assignment | statement | (function_call ";") )* RBRACE

    !?statement : IF  expression block ELSE block -> if_else
                | IF  expression block -> if_
                | WHILE expression block -> while_
                
    
    ?expression  : logic_less_priority

    !?logic_less_priority : logic_high_priority
                        | logic_less_priority "||" logic_high_priority -> or_
    
    !?logic_high_priority : clause
                        | logic_high_priority "&&" clause -> and_
    
    !?clause  : arith_less_priority
            | arith_less_priority "=" arith_less_priority -> equal
            | arith_less_priority "!=" arith_less_priority -> not_equal
            | arith_less_priority "<" arith_less_priority -> lt
            | arith_less_priority ">" arith_less_priority -> gt
            | arith_less_priority "<=" arith_less_priority -> lte
            | arith_less_priority ">=" arith_less_priority -> gte
    
    !?arith_less_priority : arith_high_priority
                        | arith_less_priority "+" arith_high_priority   -> add
                        | arith_less_priority "-" arith_high_priority   -> sub

    !?arith_high_priority : atom
                        | arith_high_priority "^" arith_high_priority -> power
                        | arith_high_priority "*" atom  -> mul
                        | arith_high_priority "/" atom  -> div
                        | arith_high_priority "%" atom  -> mod
    
    ?parenthesized_expression: "(" expression ")"
    !?atom    : INT       -> int_lit
            | FLOAT     -> float_lit
            | BOOLEAN   -> boolean_lit
            | NAME      -> id
            | STRING    -> string  
            | CHAR      -> char_lit
            | "-" atom -> unary_minus
            | "!" atom -> not_
            | parenthesized_expression     
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
    ELSE.4: "else"
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
    FROM: "from"
    STAR: "*"

    COMMENT: /\#[^\n]+/x

    %import common.NEWLINE
    %import common.WS_INLINE

    %ignore /\s+/
    %ignore COMMENT
    %ignore NEWLINE

"""


parser = Lark(plush_grammar,parser="lalr", transformer=PlushTree())
# parser = Lark(plush_grammar,parser="lalr")

def import_functions(ast, imported_functions : list, imported):
    """
    Returns the given ast with the nodes of the definitions of the imported functions.
    """
    for node in ast.defs_or_decls:
        if isinstance(node, Import):
            file = open( node.file + ".pl","r")
            other_ast = parser.parse(file.read().strip())
            other_ast = import_functions(other_ast, imported_functions, imported)
            if node.func_names == ["*"]:
                for other_node in other_ast.defs_or_decls:
                    if isinstance(other_node, FunctionDefinition) and other_node not in imported_functions:
                        imported_functions.append(other_node)
                        imported.add(other_node.name)
            else:
                for function_name in node.func_names:
                    for other_node in other_ast.defs_or_decls:
                        if isinstance(other_node, FunctionDefinition) and other_node.name == function_name:
                            imported_functions.append(other_node)
                            imported.add(function_name)
                            break
                    if function_name not in imported:
                        print(f"Function {function_name} not found in {node.file}")
                        sys.exit(1)
    ast.defs_or_decls += tuple(imported_functions)
    ast.defs_or_decls = list(filter(lambda x: not isinstance(x, Import), ast.defs_or_decls))
    return ast


def parse_plush(program : str):
    try:
        ast = parser.parse(program.strip())
    except LarkError as e:
        line = e.line
        column = e.column
        column_end = column + len(e.token)
        print(f"Unexpected token ({e.token}) at line {line}, column {column} to {column_end} in program") 
        sys.exit(1)


    # add imported functions to the tree
    imported_functions = []
    imported = set()
    ast = import_functions(ast, imported_functions, imported)
    return ast

if __name__ == "__main__":
    # Example usage:
    program = """
        val x : int;
    """

    file = open("/home/alexandref/FCUL/compilers/plush_compiler/my_program.pl","r")
    program = file.read()
    tree = parse_plush(program)
    print()
    # print(tree.pretty())
    for node in tree.defs_or_decls:
        print(node.text)