# Plush Compiler

By Alexandre Figueiredo fc57099

Using LLVM 14.0

Need -no-pier for compiling .ll files with clang

## Project Structure

plush_parser.py: Contains the logic of the parser. It's where the grammar and the logic for the imports are.
ast_nodes.py: Contains the definition of the nodes the AST. Also contains the function to represent a node as JSN.
tree_transformer.py: Contains the logic of how to build the AST, with the rules of the grammar in (plush_parser.py). Here is also where the logic of unparsing nodes and storing their positions in the program is, for the purpose of showing better error messages.
type_checker.py: Contains the logic of checking the semantics of the program. Uses the data processed in tree_transformer.py to display better error messages.
interpreter.py: Incomplete implementation of an interpreter for plush. Only used to test if the AST structure was correct, thus being incomplete.
plush_functions.c: Contains the C implementation of the predefined functions in plush.
pre_def_funcs.ll: Contains the declarations of the plush predefined functions, in LLVM IR format
compiler.py: Contains the logic to generate the LLVM code, from the AST, and runs the result.

## How to use

run './setup.sh' to build the container that has the compiler
run ./plush <program_file> <--tree>

The <program_file> is the file where your main function.
The <--tree> arg is optional, use in case you want to see a JSON representation of the programs AST.

Before running plush, make sure to run the setup.sh if you did any changes!

Example of usage:

1. Write a plush program in a file named my_program.pl
2. run ./setup.sh
3. run ./plush my_program.pl
4. If you want to see the program's AST in a JSON format, run ./plush my_program.pl --tree

## Predefined functions

These are functions that are available in plush:

print_int(val int x)

print_float(val float x)

print_string(val string s)

print_char(val char c)

print_boolean(val boolean x)

print_int_array(val [int] arr, val int size)

print_float_array(val [float] arr, val int size)

print_string_array(val [string] arr, val int size)

print_char_array(val [char] arr, val int size)

print_boolean_array(val [boolean] arr, val int size)

power_int(val int base, val int e) : int

power_float(val float base, val float e) : float

get_int_array(val int size) : [int]

get_string_array(val int size) : [string]

get_float_array(val int size) : [float]

get_char_array(val int size) : [char]

get_boolean_array(val int size) : [boolean]

get_int_matrix(val int row, val int col) : [[int]]

get_float_matrix(val int row, val int col) : [[float]]

get_string_matrix(val int row, val int col) : [[string]]

get_char_matrix(val int row, val int col) : [[char]]

get_boolean_matrix(val int row, val int col) : [[boolean]]

## How to add new predefined functions

1. Write a C implementation of the function wanted, and add it to the file plush_functions.c
2. Add the LLVM declaration of the function to the file pre_def_func.ll
3. Go to the type_checker.py file and add the function to the Context in the function add_pred_def_funcs, like : ctx.add_function(("func_name",[ValParam(name="param1", type* = ParamType())],ReturnType()), False)

### Extras

1. You can import functions from other .pl files, by adding to your code 'from file_name import functions', you can type \* to import all functions of the file
2. There are error messages so you can understand more clearly whats the problem.
