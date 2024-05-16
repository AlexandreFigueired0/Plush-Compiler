declare void @print_int(i32)

declare void @print_float(float)

declare void @print_string(i8*)

declare void @print_char(i8)

declare void @print_boolean(i1)

declare void @print_int_array(i32*, i32)

declare i32 @power_int(i32 , i32)

declare i32* @get_int_array(i32)

declare i8** @get_string_array(i32)

declare i32** @get_int_matrix(i32,i32)
define void @main(i8** %args) {
	%args1 = alloca i8**
	store i8** %args, i8*** %args1
	%c2 = alloca i8
	store i8 99, i8* %c2
	%tmp_3 = load i8, i8* %c2
	call void @print_char( i8  %tmp_3 )
	ret void
}