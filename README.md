# Plush Compiler

By Alexandre Figueiredo fc57099

Using LLVM 14.0

Need -no-pier for compiling .ll files with clang

## Predefined functions

#include <stdio.h>
#include <math.h>
#include <stdlib.h>

print_int(int x)

print_float(float x)

print_string(string s)

print_char(char c)

print_boolean(boolean x)

print_int_array([int] arr, int size)

print_float_array([float] arr, int size)

print_string_array([string] arr, int size)

print_char_array([char] arr, int size)

print_boolean_array([boolean] arr, int size)

power_int(int base, int e) : int

power_float(float base, float e) : float

get_int_array(int size) : [int]

get_string_array(int size) : [string]

get_float_array(int size) : [float]

get_char_array(int size) : [char]

get_boolean_array(int size) : [boolean]

get_int_matrix(int row, int col) : [[int]]

get_float_matrix(int row, int col) : [[float]]

get_string_matrix(int row, int col) : [[string]]

get_char_matrix(int row, int col) : [[char]]

get_boolean_matrix(int row, int col) : [[boolean]]

## How to add new predefined functions

1. Add a C implementaion of the function wanted, and added it to the file plush_functions.c
2. Add the LLVM declaration of the function to the file pre_def_func.ll
3. Go to the type*checker.py file and add the function to the Context in the function add_pred_def_funcs, like : ctx.add_function(("func_name",[ValParam(name="param1", type* = ParamType())],ReturnType()), False)
