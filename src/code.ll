declare void @print_int(i32)

declare i32 @power_int(i32 , i32)

define void @main() {
	call void @hello(  )
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
	%tmp_13 = call i32 @power_int(i32 %tmp_12, i32 2)
	call void @print_int( i32  %tmp_13 )
	ret void
}
define void @hello() {
	call void @print_int( i32  1 )
	ret void
}