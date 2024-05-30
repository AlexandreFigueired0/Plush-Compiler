from lark import Lark
from tree_transformer import PlushTree
from ast_nodes import *
import sys



plush_grammar = f"""
    start: (function_declaration | val_definition | var_definition | function_definition | import_)*

    ?import_: FROM NAME "import" imported_functions
    imported_functions: (NAME ("," NAME)*) | STAR
    ?function_declaration: "function" NAME "(" params ")" (":" type)? ";" -> function_declaration
    ?function_definition: "function" NAME "(" params ")" (":" type)? block -> function_definition
    
    ?definition : val_definition
                | var_definition
                | assignment
                | array_position_assignment
    
    ?assignment : NAME ":=" expression ";" -> assignment
    ?array_position_assignment: NAME ("[" expression "]")+ ":=" expression ";"

    ?val_definition  : "val" NAME ":" type ":=" expression ";"
    ?var_definition  : "var" NAME ":" type  ":=" expression ";"
    
    params: param ("," param)*
            |
    param  : "val" NAME ":" type  -> val_param
            | "var" NAME ":" type  -> var_param

    block: "{{" ( val_definition | var_definition | assignment | array_position_assignment | statement | (function_call ";") )* "}}"

    ?statement  : "if"  expression block -> if_
                | "if"  expression block "else" block -> if_else
                | "while" expression block -> while_
                
    
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

    function_call: NAME "(" concrete_params ")"
    ?array_access: (NAME|function_call) ("[" expression "]")+
    concrete_params: expression ("," expression)*  
                    |
    
    ?type: "int" -> int_type
        | "float" -> float_type
        | "double" -> double_type
        | "string" -> string_type
        | "char" -> char_type
        | "boolean" -> boolean_type
        | "[" type "]" -> array_type
    

    INT.1: /[0-9](_*[0-9])*/
    FLOAT.2: /[0-9]*\.[0-9]+/
    BOOLEAN.3: /true|false/
    STRING: /\"[^"]*\"/
    CHAR: /\'[^']\'/
    NAME: /[a-zA-Z_][a-zA-Z0-9_]*/
    FROM: "from"
    STAR: "*"

    COMMENT: /\#[^\n]+/x

    %import common.NEWLINE
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
    ast = parser.parse(program.strip())

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

    file = open("/home/alexandref/compilers/plush_compiler/my_program.pl","r")
    program = file.read()
    tree = parse_plush(program)
    print()
    # print(tree.pretty())
    for node in tree.defs_or_decls:
        print(node)