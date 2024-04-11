from lark import Lark

plush_grammar = """
    start: (declaration | definition)*

    ?declaration: val_declaration
                | var_declaration
                | "function" NAME "(" params ")" (":" type)? ";" -> function_declaration
    
    ?definition : val_definition
                | var_definition
                | "function" NAME "(" params ")" (":" type)? block -> function_definition
                | assignment
                | array_position_assignment
    
    ?assignment  : NAME ":=" expression ";" -> assignment
    ?array_position_assignment: NAME "[" expression "]" ":=" expression ";"

    ?val_definition  : "val" NAME ":" type ":=" expression ";"
    ?var_definition  : "var" NAME ":" type  ":=" expression ";"
    
    ?val_declaration: "val" NAME ":" type ";" 
    ?var_declaration: "var" NAME ":" type  ";"
    
    params: param ("," param)*
            |
    param  : "val" NAME ":" type  -> val_param
            | "var" NAME ":" type  -> var_param

    block: "{" ( var_declaration | var_declaration | val_definition | var_definition | assignment | array_position_assignment | statement | (function_call ";") )* "}"

    ?statement  : "if"  expression block -> if
                | "if"  expression block "else" block -> if_else
                | "while" expression block -> while
                
    
    ?expression  : logic_less_priority

    ?logic_less_priority : logic_high_priority
                        | logic_less_priority "||" logic_high_priority -> or
    
    ?logic_high_priority : clause
                        | logic_high_priority "&&" clause -> and
    
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
            | "-" atom -> unary_minus
            | "!" atom -> not
            | "(" logic_less_priority ")"     
            | array_access 
            | function_call

    ?array_access: NAME "[" expression "]"  
    function_call: NAME "(" concrete_params ")"
    concrete_params: expression ("," expression)*  
                    |
    
    ?type: "int" -> int_type
        | "float" -> float_type
        | "double" -> double_type
        | "string" -> string_type
        | "boolean" -> boolean_type
        | "[" type "]" -> array_type
    
    NAME: /(?!(true|false))[a-zA-Z_][a-zA-Z0-9_]*/

    INT: /[0-9](_*[0-9])*/
    FLOAT: /[0-9]*\.[0-9]+/
    STRING: /\"[^"]*\"/
    BOOLEAN: "true" | "false"

    COMMENT: /\#[^\n]+/x

    %import common.NEWLINE
    %ignore /\s+/
    %ignore COMMENT
    %ignore NEWLINE

"""
# TODO: regex dos ints
# TODO: true e false estao a ser reconhecidos como variaveis
# TODO: simplificar a arvore resolvida, os ? ajudaram muito mas nao percebi o que fazem, há mais formas

parser = Lark(plush_grammar,parser="lalr")

def parse_plush(program : str):
    return parser.parse(program.strip())


if __name__ == "__main__":
    # Example usage:
    program = """
        val x: int :=1;
        function main(val y: int, var z: boolean){
        
            var a : int := 1* (3^5 + 2) - 3;
            a := a || true;
            sum();

            if(1 < 2) {
                a := 3;
            } else {
                a := b[1];
                b[1] := 3;
            }
        }
        function sum();
    """

    # file = open("../../plush_testsuite/0_valid/maxRangeSquared.pl","r")
    # program = file.read()
    tree = parse_plush(program)
    print(tree.pretty())
    # print(tree)