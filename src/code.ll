@actual_min1 = dso_local global i32 -9
@actual_max3 = dso_local global i32 9
declare void @print_int(i32)

declare void @print_float(float)

declare void @print_string(i8*)

declare void @print_char(i8)

declare void @print_boolean(i1)

declare void @print_int_array(i32*, i32)

declare void @print_float_array(float*, i32)

declare void @print_string_array(i8**, i32)

declare void @print_char_array(i8*, i32)

declare void @print_boolean_array(i1*, i32)

declare i32 @power_int(i32 , i32)

declare float @power_float(float,float)

declare i32* @get_int_array(i32)

declare float* @get_float_array(i32)

declare i8** @get_string_array(i32)

declare i8* @get_char_array(i32)

declare i1* @get_boolean_array(i32)

declare i32** @get_int_matrix(i32,i32)

declare float** @get_float_matrix(i32,i32)

declare i8*** @get_string_matrix(i32,i32)

declare i8** @get_char_matrix(i32,i32)

declare i1** @get_boolean_matrix(i32,i32)
define i32 @maxRangeSquared(i32 %mi, i32 %ma) {
	%maxRangeSquared6 = alloca i32
	%mi4 = alloca i32
	%ma5 = alloca i32
	store i32 %mi, i32* %mi4
	store i32 %ma, i32* %ma5
	%current_max7 = alloca i32
	%tmp_8 = load i32, i32* %mi4
	%tmp_9 = call i32 @power_int(i32 %tmp_8, i32 2)
	store i32 %tmp_9, i32* %current_max7
	br label %while_cond10
while_cond10:
	%tmp_13 = load i32, i32* %mi4
	%tmp_14 = load i32, i32* %ma5
	%tmp_15 = icmp sle i32 %tmp_13, %tmp_14
	br i1 %tmp_15, label %while_body11, label %while_end12
while_body11:
	%current_candidate16 = alloca i32
	%tmp_17 = load i32, i32* %mi4
	%tmp_18 = call i32 @power_int(i32 %tmp_17, i32 2)
	store i32 %tmp_18, i32* %current_candidate16
	%tmp_19 = load i32, i32* %current_candidate16
	%tmp_20 = load i32, i32* %current_max7
	%tmp_21 = icmp sgt i32 %tmp_19, %tmp_20
	br i1 %tmp_21, label %if_true22, label %if_end23
if_true22:
	%tmp_24 = load i32, i32* %current_candidate16
	store i32 %tmp_24, i32* %current_max7
	br label %if_end23
if_end23:
	%tmp_25 = load i32, i32* %mi4
	%tmp_26 = add i32 %tmp_25, 1
	store i32 %tmp_26, i32* %mi4
	br label %while_cond10
while_end12:
	%tmp_27 = load i32, i32* %current_max7
	store i32 %tmp_27, i32* %maxRangeSquared6
	%tmp_28 = load i32, i32* %maxRangeSquared6
	ret i32 %tmp_28
}
define void @main(i8** %args) {
	%args29 = alloca i8**
	store i8** %args, i8*** %args29
	%result30 = alloca i32
	%tmp_31 = load i32, i32* @actual_min1
	%tmp_32 = load i32, i32* @actual_max3
	%maxRangeSquared_33 = call i32 @maxRangeSquared( i32  %tmp_31, i32  %tmp_32 )
	store i32 %maxRangeSquared_33, i32* %result30
	%tmp_34 = load i32, i32* %result30
	call void @print_int( i32  %tmp_34 )
	ret void
}