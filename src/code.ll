@pl_str_3 = private unnamed_addr constant [4 x i8] c"Bye\00" 
@pl_str_2 = private unnamed_addr constant [13 x i8] c"Hello World!\00" 
declare void @print_int(i32)

declare void @print_float(float)

declare void @print_string(i8*)

declare i32 @power_int(i32 , i32)

declare i32* @get_int_array(i32)

define void @main() {
	%s1 = alloca i8*
	store i8* getelementptr inbounds ([13 x i8], [13 x i8]* @pl_str_2, i64 0, i64 0), i8** %s1
	store i8* getelementptr inbounds ([4 x i8], [4 x i8]* @pl_str_3, i64 0, i64 0), i8** %s1
	%hello4 = alloca i8*
	store i8* getelementptr inbounds ([13 x i8], [13 x i8]* @pl_str_2, i64 0, i64 0), i8** %hello4
	%tmp_5 = load i8*, i8** %hello4
	call void @print_string( i8*  %tmp_5 )
	%tmp_6 = load i8*, i8** %s1
	call void @print_string( i8*  %tmp_6 )
	ret void
}