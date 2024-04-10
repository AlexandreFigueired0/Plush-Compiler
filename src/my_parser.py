from lark import Lark

plush_grammar = """
    start: (declaration | definition | function_call ";")*

    declaration : val_declaration
                | var_declaration
                | function_signature ";" -> function_declaration
    
    definition  : val_definition
                | var_definition
                | function_signature block -> function_definition
                | assignment
                | array_position_assignment
    
    assignment  : NAME ASSIGN expression ";" -> assignment
    array_position_assignment: NAME "[" expression "]" ASSIGN expression ";"

    val_definition  : val_signature ASSIGN expression ";" -> val_definition
    var_definition  : var_signature ASSIGN expression ";" -> var_definition
    
    val_declaration: val_signature ";" -> val_declaration
    var_declaration: var_signature ";" -> var_declaration
    
    var_signature  : VAR NAME ":" type -> var_signature
    val_signature  : VAL NAME ":" type -> val_signature

    list_params: (val_signature | var_signature) ("," (val_signature | var_signature))*

    function_signature: FUNCTION NAME "(" (list_params)? ")" (":" type)?
    
    block: "{" (val_definition | val_declaration | var_definition| var_declaration | assignment |statement)* "}"

    statement   : IF  expression block (ELSE block)? -> if_statement
                | WHILE expression block -> while_statement
    
    expression  : logic_less_priority

    logic_less_priority : logic_high_priority
                        | logic_less_priority OR logic_high_priority -> or
    
    logic_high_priority : clause
                        | logic_high_priority AND clause -> and
    
    clause  : arith_less_priority
            | arith_less_priority EQUAL arith_less_priority -> equal
            | arith_less_priority NOT_EQUAL arith_less_priority -> not_equal
            | arith_less_priority LT arith_less_priority -> lt
            | arith_less_priority GT arith_less_priority -> gt
            | arith_less_priority LTE arith_less_priority -> lte
            | arith_less_priority GTE arith_less_priority -> gte
    

    arith_less_priority : arith_high_priority
                        | arith_less_priority "+" arith_high_priority   -> add
                        | arith_less_priority "-" arith_high_priority   -> sub

    arith_high_priority : atom
                        | arith_high_priority "^" arith_high_priority -> power
                        | arith_high_priority "*" atom  -> mul
                        | arith_high_priority "/" atom  -> div
                        | arith_high_priority "%" atom  -> mod
    
    atom    : INT       -> int
            | FLOAT     -> float
            | NAME      -> var
            | BOOLEAN   -> boolean  
            | STRING    -> string  
            | "-" atom -> unary_minus
            | "!" atom -> not
            | "(" logic_less_priority ")" -> parenthesis     
            | array_access 
            | function_call

    array_access: NAME "[" expression "]"  
    function_call: NAME "(" (expression ("," expression)*)? ")"   
    
    type: "int" -> int_type
        | "float" -> float_type
        | "double" -> double_type
        | "string" -> string_type
        | "boolean" -> boolean_type
        | "[" type "]" -> array_type
    
    NAME: /[a-zA-Z_][a-zA-Z0-9_]*/
    IF  : "if"
    ELSE: "else"
    WHILE: "while"
    FUNCTION: "function"

    INT: /[0-9](_*[0-9])*/
    FLOAT: /[0-9]*\.[0-9]+/
    STRING: /\"[^"]*\"/
    BOOLEAN: "true" | "false"

    VAL: "val"
    VAR: "var"
    ASSIGN: ":="
    OR: "||"
    AND: "&&"
    EQUAL: "="
    NOT_EQUAL: "!="
    LT: "<"
    LTE: "<="
    GT: ">"
    GTE: ">="
    NEG: "!"
    COMMENT: /\#[^\r\n]+/x

    %import common.NEWLINE
    %ignore /\s+/
    %ignore COMMENT
    %ignore NEWLINE

"""
# TODO: regex dos ints
# TODO: true e false estao a ser reconhecidos como variaveis
# TODO: verificar que if e whiles so funcionam dentro de funcs

parser = Lark(plush_grammar,parser="lalr")

def parse_plush(program : str):
    return parser.parse(program.strip())


if __name__ == "__main__":
    # Example usage:
    program = """
        val x: int := 5;
    """

    # file = open("../../plush_testsuite/0_valid/maxRangeSquared.pl","r")
    # program = file.read()
    tree = parse_plush(program)
    print(tree.pretty())
    # print(tree)