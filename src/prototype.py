# start: declaration*

#     declaration: const_decl
#                | var_decl
#                | func_decl

#     const_decl: VAL NAME ":" type DEF expression ";"
#     var_decl: VAR NAME ":" type DEF expression ";"
#     func_decl: FUNCTION NAME "(" param_list? ")" ":" type block | FUNCTION NAME "(" param_list? ")" ":" type ";"
    
#     param_list: param ("," param)*
#     param: "val" NAME ":" type
    
#     block: "{" statement* "}"
    
#     statement: assignment
#              | if_statement
#              | while_statement
#              | block
    
#     assignment: const_decl | var_decl | NAME ":=" expression ";" -> assign
#     if_statement: IF "(" expression ")" block (ELSE block)?
#     while_statement: WHILE "(" expression ")" block
    
#     expression: expression ("+" | "-" | "*" | "/" | "%" | "<" | "<=" | ">" | ">=" | "==" | "!=" | "&&" | "||") expression
#                | "-" expression
#                | "!" expression
#                | literal
#                | NAME
#                | NAME "[" INT "]"
#                | "(" expression ")"