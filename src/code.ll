declare void @print_int(i32)

declare void @print_float(float)

declare void @print_string(i8*)

declare void @print_boolean(i1)

declare i32 @power_int(i32 , i32)

declare i32* @get_int_array(i32)

declare i32** @get_int_matrix(i32,i32)
define void @main() {
	%m1 = alloca i32**
	%tmp_2 = call i32** @get_int_matrix( i32  3, i32  3 )
	store i32** %tmp_2, i32*** %m1
	%tmp_3 = load i32**, i32*** %m1
	%midxtmp_4 = getelementptr i32*, i32** %tmp_3, i32 0
	%tmp_5 = load i32*, i32** %midxtmp_4
	%midxtmp_6 = getelementptr i32, i32* %tmp_5, i32 0
	%tmp_7 = load i32, i32* %midxtmp_6
	call void @print_int( i32  %tmp_7 )
	ret void
}