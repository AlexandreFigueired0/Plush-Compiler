@value1 = dso_local global i32 16
declare void @print_int(i32)

declare void @print_float(float)

declare void @print_string(i8*)

declare void @print_char(i8)

declare void @print_boolean(i1)

declare void @print_int_array(i32*, i32)

declare i32 @power_int(i32 , i32)

declare i32* @get_int_array(i32)

declare i8** @get_string_array(i32)

declare i32** @get_int_matrix(i32,i32)
define i1 @isPerfectSquare(i32 %n) {
	%isPerfectSquare3 = alloca i1
	%n2 = alloca i32
	store i32 %n, i32* %n2
	%result4 = alloca i1
	store i1 false, i1* %result4
	%low5 = alloca i32
	store i32 1, i32* %low5
	%high6 = alloca i32
	%tmp_7 = load i32, i32* %n2
	store i32 %tmp_7, i32* %high6
	br label %while_cond8
while_cond8:
	%tmp_11 = load i32, i32* %low5
	%tmp_12 = load i32, i32* %high6
	%tmp_13 = icmp sle i32 %tmp_11, %tmp_12
	%tmp_14 = load i1, i1* %result4
	%tmp_15 = xor i1 %tmp_14, 1
	%tmp_16 = and i1 %tmp_13, %tmp_15
	br i1 %tmp_16, label %while_body9, label %while_end10
while_body9:
	%mid17 = alloca i32
	%tmp_18 = load i32, i32* %low5
	%tmp_19 = load i32, i32* %high6
	%tmp_20 = load i32, i32* %low5
	%tmp_21 = sub i32 %tmp_19, %tmp_20
	%tmp_22 = sdiv i32 %tmp_21, 2
	%tmp_23 = add i32 %tmp_18, %tmp_22
	store i32 %tmp_23, i32* %mid17
	%square24 = alloca i32
	%tmp_25 = load i32, i32* %mid17
	%tmp_26 = load i32, i32* %mid17
	%tmp_27 = mul i32 %tmp_25, %tmp_26
	store i32 %tmp_27, i32* %square24
	%tmp_28 = load i32, i32* %square24
	%tmp_29 = load i32, i32* %n2
	%tmp_30 = icmp eq i32 %tmp_28, %tmp_29
	br i1 %tmp_30, label %if_true31, label %if_end32
if_true31:
	store i1 true, i1* %result4
	br label %if_end32
if_end32:
	%tmp_33 = load i32, i32* %square24
	%tmp_34 = load i32, i32* %n2
	%tmp_35 = icmp ne i32 %tmp_33, %tmp_34
	%tmp_36 = load i32, i32* %square24
	%tmp_37 = load i32, i32* %n2
	%tmp_38 = icmp slt i32 %tmp_36, %tmp_37
	%tmp_39 = and i1 %tmp_35, %tmp_38
	br i1 %tmp_39, label %if_true40, label %if_end41
if_true40:
	%tmp_42 = load i32, i32* %mid17
	%tmp_43 = add i32 %tmp_42, 1
	store i32 %tmp_43, i32* %low5
	br label %if_end41
if_end41:
	%tmp_44 = load i32, i32* %square24
	%tmp_45 = load i32, i32* %n2
	%tmp_46 = icmp ne i32 %tmp_44, %tmp_45
	%tmp_47 = load i32, i32* %square24
	%tmp_48 = load i32, i32* %n2
	%tmp_49 = icmp slt i32 %tmp_47, %tmp_48
	%tmp_50 = xor i1 %tmp_49, 1
	%tmp_51 = and i1 %tmp_46, %tmp_50
	br i1 %tmp_51, label %if_true52, label %if_end53
if_true52:
	%tmp_54 = load i32, i32* %mid17
	%tmp_55 = sub i32 %tmp_54, 1
	store i32 %tmp_55, i32* %high6
	br label %if_end53
if_end53:
	br label %while_cond8
while_end10:
	%tmp_56 = load i1, i1* %result4
	store i1 %tmp_56, i1* %isPerfectSquare3
	%tmp_57 = load i1, i1* %isPerfectSquare3
	ret i1 %tmp_57
}
define void @main(i8** %args) {
	%args58 = alloca i8**
	store i8** %args, i8*** %args58
	%result59 = alloca i1
	%tmp_60 = load i32, i32* @value1
	%tmp_61 = call i1 @isPerfectSquare( i32  %tmp_60 )
	store i1 %tmp_61, i1* %result59
	%tmp_62 = load i1, i1* %result59
	call void @print_boolean( i1  %tmp_62 )
	ret void
}