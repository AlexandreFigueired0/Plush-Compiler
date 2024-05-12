declare void @print_int(i32)

declare i32 @power_int(i32 , i32)

declare i32* @get_int_array(i32)

define void @main() {


	%x1 = alloca i32
	%tmp_2 = sub i32 0, 1
	store i32 %tmp_2, i32* %x1
	br label %while_cond3
while_cond3:
	%tmp_6 = load i32, i32* %x1
	%tmp_7 = icmp slt i32 %tmp_6, 5
	br i1 %tmp_7, label %while_body4, label %while_end5
while_body4:
	%tmp_8 = load i32, i32* %x1
	call void @print_int( i32  %tmp_8 )
	%tmp_9 = load i32, i32* %x1
	%tmp_10 = add i32 %tmp_9, 1
	store i32 %tmp_10, i32* %x1
	br label %while_cond3
while_end5:
	%tmp_11 = load i32, i32* %x1
	call void @print_int( i32  %tmp_11 )
	%tmp_12 = load i32, i32* %x1
	%tmp_13 = call i32 @mult( i32  %tmp_12, i32  2 )
	call void @print_int( i32  %tmp_13 )
	ret void
}
define i32 @mult(i32 %x, i32 %y) {
	%mult16 = alloca i32
	%x14 = alloca i32
	%y15 = alloca i32
	store i32 %x, i32* %x14
	store i32 %y, i32* %y15
	%tmp_17 = load i32, i32* %x14
	%tmp_18 = load i32, i32* %y15
	%tmp_19 = mul i32 %tmp_17, %tmp_18
	store i32 %tmp_19, i32* %mult16
	%tmp_20 = load i32, i32* %mult16
	ret i32 %tmp_20
}