@.casual_str_cas_1 = private unnamed_addr constant [4 x i8] c"%d\0A\00", align 1
declare i32 @printf(i8*, ...) #1
define i32 @main() {
	%ptr_x = alloca i32
	store i32 18, i32* %ptr_x
   %cas_2 = load i32, i32* %ptr_x
	%cas_3 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.casual_str_cas_1, i64 0, i64 0), i32 %cas_2)
	ret i32 0
}