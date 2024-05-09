@.str = private unnamed_addr constant [4 x i8] c"%d\0A\00", align 1
declare i32 @printf(i8*, ...)

define void @print_int(i32 noundef %x) {
entry:
  %x.addr = alloca i32, align 4
  store i32 %x, i32* %x.addr, align 4
  %0 = load i32, i32* %x.addr, align 4
  %call = call i32 (i8*, ...) @printf(i8* noundef getelementptr inbounds ([4 x i8], [4 x i8]* @.str, i64 0, i64 0), i32 noundef %0)
  ret void
}
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
	ret void
}