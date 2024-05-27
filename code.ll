@.pl_str_2 = private unnamed_addr constant [5 x i8] c"test\00" 
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
define void @main() {
	%x1 = alloca i8*
	store i8* getelementptr inbounds ([5 x i8], [5 x i8]* @.pl_str_2, i64 0, i64 0), i8** %x1
	%x_a3 = alloca i8*
	%tmp_4 = load i8*, i8** %x1
	%string_to_char_array_5 = call i8* @string_to_char_array( i8*  %tmp_4 )
	store i8* %string_to_char_array_5, i8** %x_a3
	%tmp_6 = load i8*, i8** %x_a3
	%x_a_idx_7 = getelementptr i8, i8* %tmp_6, i32 0
	%tmp_8 = load i8, i8* %x_a_idx_7
	call void @print_char( i8  %tmp_8 )
	ret void
}