@.str = private unnamed_addr constant [3 x i8] c"%d\00", align 1
declare i32 @printf(i8*, ...)

define void @print_int(i32 noundef %x) {
entry:
  %x.addr = alloca i32, align 4
  store i32 %x, i32* %x.addr, align 4
  %0 = load i32, i32* %x.addr, align 4
  %call = call i32 (i8*, ...) @printf(i8* noundef getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i64 0, i64 0), i32 noundef %0)
  ret void
}
define void @main() {
	%x1 = alloca i32
   %tmp_2 = add i32 1, 1
	store i32 %tmp_2, i32* %x1
	%tmp_3 = load i32, i32* %x1
	%tmp_4 = icmp sgt i32 %tmp_3, 2
	br i1 %tmp_4, label %if_true5, label %if_end6
if_true5:
	store i32 1, i32* %x1
	br label %if_end6
if_end6:
	%tmp_7 = load i32, i32* %x1
	call void @print_int( i32  %tmp_7 )
	ret void
}