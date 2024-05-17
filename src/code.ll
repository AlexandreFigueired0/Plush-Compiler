@.pl_str_8 = private unnamed_addr constant [6 x i8] c"Hello\00" 
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
	%strings1 = alloca i8***
	%get_string_matrix_2 = call i8*** @get_string_matrix( i32  3, i32  3 )
	store i8*** %get_string_matrix_2, i8**** %strings1
	%tmp_3 = load i8***, i8**** %strings1
	%strings_idx_4 = getelementptr i8**, i8*** %tmp_3, i32 0
	%tmp_5 = load i8**, i8*** %strings_idx_4
	%strings_idx_6 = getelementptr i8*, i8** %tmp_5, i32 0
	%tmp_7 = load i8*, i8** %strings_idx_6
	store i8* getelementptr inbounds ([6 x i8], [6 x i8]* @.pl_str_8, i64 0, i64 0), i8** %strings_idx_6
	ret void
}