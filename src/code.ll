declare void @print_int(i32)

declare void @print_float(float)

declare void @print_string(i8*)

declare i32 @power_int(i32 , i32)

declare i32* @get_int_array(i32)

define void @main() {
	%a1 = alloca i32*
	%tmp_2 = call i32* @get_int_array( i32  12 )
	store i32* %tmp_2, i32** %a1
	%tmp_3 = load i32*, i32** %a1
	%aidxtmp_4 = getelementptr i32, i32* %tmp_3, i32 4
	%tmp_6 = sub i32 0, 2
	store i32 %tmp_6, i32* %aidxtmp_4
	%tmp_7 = load i32*, i32** %a1
	%aidxtmp_8 = getelementptr i32, i32* %tmp_7, i32 4
	%tmp_9 = load i32, i32* %aidxtmp_8
	call void @print_int( i32  %tmp_9 )
	ret void
}