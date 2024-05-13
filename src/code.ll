declare void @print_int(i32)

declare i32 @power_int(i32 , i32)

declare i32* @get_int_array(i32)

define void @main() {
	%x1 = alloca i32*
	%tmp_2 = call i32* @get_int_array( i32  5 )
	store i32* %tmp_2, i32** %x1
	%tmp_3 = load i32*, i32** %x1
	%xidxtmp_4 = getelementptr i32, i32* %tmp_3, i32 0
	store i32 10, i32* %xidxtmp_4
	%i6 = alloca i32
	%tmp_7 = load i32*, i32** %x1
	%xidxtmp_8 = getelementptr i32, i32* %tmp_7, i32 0
	%tmp_9 = load i32, i32* %xidxtmp_8
	store i32 %tmp_9, i32* %i6
	%tmp_10 = load i32, i32* %i6
	call void @print_int( i32  %tmp_10 )
	ret void
}
define i32 @mult(i32 %x, i32 %y) {
	%mult13 = alloca i32
	%x11 = alloca i32
	%y12 = alloca i32
	store i32 %x, i32* %x11
	store i32 %y, i32* %y12
	%tmp_14 = load i32, i32* %x11
	%tmp_15 = load i32, i32* %y12
	%tmp_16 = mul i32 %tmp_14, %tmp_15
	store i32 %tmp_16, i32* %mult13
	%tmp_17 = load i32, i32* %mult13
	ret i32 %tmp_17
}
define i32* @a() {
	%a18 = alloca i32*
	%x19 = alloca i32*
	%tmp_20 = call i32* @get_int_array( i32  5 )
	store i32* %tmp_20, i32** %x19
	%tmp_21 = load i32*, i32** %x19
	store i32* %tmp_21, i32** %a18
	%tmp_22 = load i32*, i32** %a18
	ret i32* %tmp_22
}