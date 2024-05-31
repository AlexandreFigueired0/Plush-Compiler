declare void @print_int(i32)

declare void @print_float(float)

declare void @print_string(i8*)

declare void @print_char(i8)

declare void @print_boolean(i1)

declare void @print_int_array(i32*, i32)

declare void @print_float_array(float*, i32)

declare void @print_string_array(i8**, i32)

declare void @print_char_array(i8*, i32)

declare void @print_boolean_array(i1*, i32)

declare i8* @string_to_char_array(i8*)

declare i32 @power_int(i32 , i32)

declare float @power_float(float,float)

declare i32* @get_int_array(i32)

declare float* @get_float_array(i32)

declare i8** @get_string_array(i32)

declare i8* @get_char_array(i32)

declare i1* @get_boolean_array(i32)

declare i32** @get_int_matrix(i32,i32)

declare float** @get_float_matrix(i32,i32)

declare i8*** @get_string_matrix(i32,i32)

declare i8** @get_char_matrix(i32,i32)

declare i1** @get_boolean_matrix(i32,i32)