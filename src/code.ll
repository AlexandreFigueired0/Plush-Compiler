@.plush_str_tmp_7 = private  constant [4 x i8] c"%d\0A\00" 
declare i32 @printf(i8*, ...) #1
define void @main() {
	%x1 = alloca i32
   %tmp_2 = add i32 1, 1
	store i32 %tmp_2, i32* %x1
   %tmp_3 = load i32, i32* %x1
	%tmp_4 = icmp sgt i32 %tmp_3, 1
	br i1 %tmp_4, label %if_true5, label %if_false6


if_true5:
   %tmp_8 = load i32, i32* %x1
	%tmp_9 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.plush_str_tmp_7, i64 0, i64 0), i32 %tmp_8)


	ret void
}