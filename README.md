# Plush Compiler

By Alexandre Figueiredo fc57099

Using LLVM 14.0

Need -no-pier for compiling .ll files with clang

## Predefined functions

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

1. Add a C implementaion of the function wanted, and added it to the file plush_functions.c
2. Add the LLVM declaration of the function to the file pre_def_func.ll
3. Go to the type_checker.py file and add the function to the Context in the function add_pred_def_funcs, like : ctx.add_function(("func_name",[ValParam(name="param1", type* = ParamType())],ReturnType()), False)
