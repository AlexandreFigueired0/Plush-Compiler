@.pl_str_2 = private unnamed_addr constant [5 x i8] c"Test\00" 
@x1 = dso_local global i8* getelementptr inbounds ([5 x i8], [5 x i8]* @.pl_str_2, i32 0, i32 0)
declare void @print_int(i32)

declare void @print_float(float)

declare void @print_string(i8*)

declare i32 @power_int(i32 , i32)

declare i32* @get_int_array(i32)

define void @main() {
	%tmp_3 = load i8*, i8** @x1
	call void @print_string( i8*  %tmp_3 )
	ret void
}