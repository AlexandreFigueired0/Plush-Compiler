from lark import Lark, Transformer

plush_grammar = """
    start: (declaration | definition | statement)*

    declaration : vars_declaration
                | function_signature ";" -> function_declaration
    
    definition  : vars_definition
                | function_signature block -> function_definition

    vars_definition : VAL NAME ":" type DEF expression ";" -> val_definition
                    | VAR NAME ":" type DEF expression ";" -> var_definition
                    | NAME DEF expression ";" -> assign
    
    vars_declaration: VAL NAME ":" type ";" -> val_declaration
                    | VAR NAME ":" type ";" -> var_declaration
    
    

    list_params: param ("," param)*
    param: VAL NAME ":" type

    function_signature: FUNCTION NAME "(" (list_params)? ")" ":" type
    
    block: "{" (vars_declaration | vars_definition | statement)* "}"

    statement   : IF "(" expression ")" block (ELSE block)? -> if_statement
                | WHILE "(" expression ")" block -> while_statement
    
    expression  : arithmetic_expression
                | logical_expression
                

    arithmetic_expression: arith_less_priority

    
    arith_less_priority : arith_high_priority
                        | arith_less_priority "+" arith_high_priority   -> add
                        | arith_less_priority "-" arith_high_priority   -> sub

    arith_high_priority : arithmetic_literal
                        | arith_high_priority "*" arithmetic_literal  -> mul
                        | arith_high_priority "/" arithmetic_literal  -> div
                        | arith_high_priority "%" arithmetic_literal  -> mod
                        | "-" arithmetic_literal -> neg
                        | "(" arithmetic_expression ")" -> parenthesis
    
    arithmetic_literal  : INT -> int
                        | FLOAT -> float
                        | ARITH_NAME

    logical_expression  : or_expression

    or_expression   : and_expression
                    | or_expression OR and_expression -> or
    
    and_expression  : clause
                    | and_expression AND clause -> and
    
    clause  : logic_literal
            | arithmetic_expression LT arithmetic_expression   -> lt_clause
            | arithmetic_expression LTE arithmetic_expression  -> lte_clause
            | arithmetic_expression GT arithmetic_expression   -> gt_clause
            | arithmetic_expression GTE arithmetic_expression  -> gte_clause
            | expression EQUAL expression                  -> eq_clause
            | expression NOT_EQUAL expression              -> neq_clause
            | "!" logical_expression        -> not_clause
            | "(" logical_expression ")"    -> parenthesis
            

                        
    logic_literal   : "true"    -> bool_true
                    | "false"   -> bool_false
                    | LOGIC_NAME
    
    type: "int" -> int_type
        | "float" -> float_type
        | "double" -> double_type
        | "string" -> string_type
        | "[" type "]" -> array_type
    
    IF  : "if"
    ELSE: "else"
    WHILE: "while"
    FUNCTION: "function"
    INT: /[0-9]+/
    FLOAT: /[0-9]*\.[0-9]+/
    STRING: /\"[^"]*\"/
    VAL: "val"
    VAR: "var"
    DEF: ":="
    OR: "||"
    AND: "&&"
    EQUAL: "="
    NOT_EQUAL: "!="
    LT: "<"
    LTE: "<="
    GT: ">"
    GTE: ">="
    NAME: /[a-zA-Z_][a-zA-Z0-9_]*/
    ARITH_NAME: /[a-zA-Z_][a-zA-Z0-9_]*/
    LOGIC_NAME: /[a-zA-Z_][a-zA-Z0-9_]*/
    COMMENT: /#[^\n]*\n$/x

    %import common.NEWLINE
    %ignore NEWLINE
    %ignore /\s+/

"""
#  COMENTARIOS NAO FUNCIONAM

parser = Lark(plush_grammar,parser="lalr" ,start='start')

def parse_plush(program : str):
    return parser.parse(program.strip(), lambda x: True)

# Example usage:
program = """
    var x : int;

    x := 1;

    val y : int := x || x;

    function sum(val a: int,val b: int) : int;

    function sum(val a: int, val b: int) : int {
        var c : int;
        c := a + b * 1;
        sum := c;
    }
   
"""
tree = parse_plush(program)
print(tree.pretty())