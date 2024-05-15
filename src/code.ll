@array_size1 = dso_local global i32 10
declare void @print_int(i32)

declare void @print_float(float)

declare void @print_string(i8*)

declare void @print_boolean(i1)

declare i32 @power_int(i32 , i32)

declare i32* @get_int_array(i32)

define i1 @binary_search(i32* %arr, i32 %x) {
	%binary_search4 = alloca i1
	%arr2 = alloca i32*
	%x3 = alloca i32
	store i32* %arr, i32** %arr2
	store i32 %x, i32* %x3
	%left5 = alloca i32
	store i32 0, i32* %left5
	%right6 = alloca i32
	%tmp_7 = load i32, i32* @array_size1
	%tmp_8 = sub i32 %tmp_7, 1
	store i32 %tmp_8, i32* %right6
	%ret_val9 = alloca i1
	store i1 false, i1* %ret_val9
	br label %while_cond10
while_cond10:
	%tmp_13 = load i1, i1* %ret_val9
	%tmp_14 = xor i1 %tmp_13, 1
	%tmp_15 = load i32, i32* %left5
	%tmp_16 = load i32, i32* %right6
	%tmp_17 = icmp sle i32 %tmp_15, %tmp_16
	%tmp_18 = and i1 %tmp_14, %tmp_17
	br i1 %tmp_18, label %while_body11, label %while_end12
while_body11:
	%mid19 = alloca i32
	%tmp_20 = load i32, i32* %left5
	%tmp_21 = load i32, i32* %right6
	%tmp_22 = load i32, i32* %left5
	%tmp_23 = sub i32 %tmp_21, %tmp_22
	%tmp_24 = sdiv i32 %tmp_23, 2
	%tmp_25 = add i32 %tmp_20, %tmp_24
	store i32 %tmp_25, i32* %mid19
	%tmp_26 = load i32*, i32** %arr2
	%tmp_27 = load i32, i32* %mid19
	%arridxtmp_28 = getelementptr i32, i32* %tmp_26, i32 %tmp_27
	%tmp_29 = load i32, i32* %arridxtmp_28
	%tmp_30 = load i32, i32* %x3
	%tmp_31 = icmp eq i32 %tmp_29, %tmp_30
	br i1 %tmp_31, label %if_true32, label %if_end33
if_true32:
	store i1 true, i1* %ret_val9
	br label %if_end33
if_end33:
	%tmp_34 = load i32*, i32** %arr2
	%tmp_35 = load i32, i32* %mid19
	%arridxtmp_36 = getelementptr i32, i32* %tmp_34, i32 %tmp_35
	%tmp_37 = load i32, i32* %arridxtmp_36
	%tmp_38 = load i32, i32* %x3
	%tmp_39 = icmp slt i32 %tmp_37, %tmp_38
	br i1 %tmp_39, label %if_true40, label %else41
if_true40:
	%tmp_43 = load i32, i32* %mid19
	%tmp_44 = add i32 %tmp_43, 1
	store i32 %tmp_44, i32* %left5
	br label %if_end42
else41:
	%tmp_45 = load i32, i32* %mid19
	%tmp_46 = sub i32 %tmp_45, 1
	store i32 %tmp_46, i32* %right6
	br label %if_end42
if_end42:
	br label %while_cond10
while_end12:
	%tmp_47 = load i1, i1* %ret_val9
	store i1 %tmp_47, i1* %binary_search4
	%tmp_48 = load i1, i1* %binary_search4
	ret i1 %tmp_48
}
define void @main() {
	%my_array49 = alloca i32*
	%tmp_50 = load i32, i32* @array_size1
	%tmp_51 = call i32* @get_int_array( i32  %tmp_50 )
	store i32* %tmp_51, i32** %my_array49
	%i52 = alloca i32
	store i32 0, i32* %i52
	br label %while_cond53
while_cond53:
	%tmp_56 = load i32, i32* %i52
	%tmp_57 = load i32, i32* @array_size1
	%tmp_58 = icmp slt i32 %tmp_56, %tmp_57
	br i1 %tmp_58, label %while_body54, label %while_end55
while_body54:
	%tmp_59 = load i32*, i32** %my_array49
	%tmp_60 = load i32, i32* %i52
	%my_arrayidxtmp_61 = getelementptr i32, i32* %tmp_59, i32 %tmp_60
	%tmp_63 = load i32, i32* %i52
	store i32 %tmp_63, i32* %my_arrayidxtmp_61
	%tmp_64 = load i32, i32* %i52
	%tmp_65 = add i32 %tmp_64, 1
	store i32 %tmp_65, i32* %i52
	br label %while_cond53
while_end55:
	%tmp_66 = load i32*, i32** %my_array49
	%tmp_67 = call i1 @binary_search( i32*  %tmp_66, i32  9 )
	call void @print_boolean( i1  %tmp_67 )
	ret void
}