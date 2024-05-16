@.pl_str_108 = private unnamed_addr constant [3 x i8] c"--\00" 
@.pl_str_104 = private unnamed_addr constant [4 x i8] c"row\00" 
@m1_rows1 = dso_local global i32 3
@m1_cols2 = dso_local global i32 2
@m2_rows3 = dso_local global i32 2
@m2_cols4 = dso_local global i32 2
declare void @print_int(i32)

declare void @print_float(float)

declare void @print_string(i8*)

declare void @print_boolean(i1)

declare i32 @power_int(i32 , i32)

declare i32* @get_int_array(i32)

declare i8** @get_string_array(i32)

declare i32** @get_int_matrix(i32,i32)
define i32** @matrixProduct(i32** %m1, i32** %m2) {
	%matrixProduct7 = alloca i32**
	%m15 = alloca i32**
	%m26 = alloca i32**
	store i32** %m1, i32*** %m15
	store i32** %m2, i32*** %m26
	%res8 = alloca i32**
	%tmp_9 = load i32, i32* @m1_rows1
	%tmp_10 = load i32, i32* @m2_cols4
	%tmp_11 = call i32** @get_int_matrix( i32  %tmp_9, i32  %tmp_10 )
	store i32** %tmp_11, i32*** %res8
	%m1RowIdx12 = alloca i32
	store i32 0, i32* %m1RowIdx12
	br label %while_cond13
while_cond13:
	%tmp_16 = load i32, i32* %m1RowIdx12
	%tmp_17 = load i32, i32* @m1_rows1
	%tmp_18 = icmp slt i32 %tmp_16, %tmp_17
	br i1 %tmp_18, label %while_body14, label %while_end15
while_body14:
	%m2ColIdx19 = alloca i32
	store i32 0, i32* %m2ColIdx19
	br label %while_cond20
while_cond20:
	%tmp_23 = load i32, i32* %m2ColIdx19
	%tmp_24 = load i32, i32* @m2_rows3
	%tmp_25 = icmp slt i32 %tmp_23, %tmp_24
	br i1 %tmp_25, label %while_body21, label %while_end22
while_body21:
	%m2RowIdx26 = alloca i32
	store i32 0, i32* %m2RowIdx26
	br label %while_cond27
while_cond27:
	%tmp_30 = load i32, i32* %m2RowIdx26
	%tmp_31 = load i32, i32* @m2_rows3
	%tmp_32 = icmp slt i32 %tmp_30, %tmp_31
	br i1 %tmp_32, label %while_body28, label %while_end29
while_body28:
	%tmp_33 = load i32**, i32*** %res8
	%tmp_34 = load i32, i32* %m1RowIdx12
	%residxtmp_35 = getelementptr i32, i32* %tmp_33, i32 %tmp_34
	%tmp_37 = load i32**, i32*** %res8
	%tmp_38 = load i32, i32* %m1RowIdx12
	%residxtmp_39 = getelementptr i32*, i32** %tmp_37, i32 %tmp_38
	%tmp_40 = load i32*, i32** %residxtmp_39
	%tmp_41 = load i32, i32* %m2ColIdx19
	%residxtmp_42 = getelementptr i32, i32* %tmp_40, i32 %tmp_41
	%tmp_43 = load i32, i32* %residxtmp_42
	%tmp_44 = load i32**, i32*** %m15
	%tmp_45 = load i32, i32* %m1RowIdx12
	%m1idxtmp_46 = getelementptr i32*, i32** %tmp_44, i32 %tmp_45
	%tmp_47 = load i32*, i32** %m1idxtmp_46
	%tmp_48 = load i32, i32* %m2RowIdx26
	%m1idxtmp_49 = getelementptr i32, i32* %tmp_47, i32 %tmp_48
	%tmp_50 = load i32, i32* %m1idxtmp_49
	%tmp_51 = load i32**, i32*** %m26
	%tmp_52 = load i32, i32* %m2RowIdx26
	%m2idxtmp_53 = getelementptr i32*, i32** %tmp_51, i32 %tmp_52
	%tmp_54 = load i32*, i32** %m2idxtmp_53
	%tmp_55 = load i32, i32* %m2ColIdx19
	%m2idxtmp_56 = getelementptr i32, i32* %tmp_54, i32 %tmp_55
	%tmp_57 = load i32, i32* %m2idxtmp_56
	%tmp_58 = mul i32 %tmp_50, %tmp_57
	%tmp_59 = add i32 %tmp_43, %tmp_58
	store i32 %tmp_59, i32* %residxtmp_35
	%tmp_60 = load i32, i32* %m2ColIdx19
	%residxtmp_61 = getelementptr i32, i32* %tmp_36, i32 %tmp_60
	%tmp_63 = load i32**, i32*** %res8
	%tmp_64 = load i32, i32* %m1RowIdx12
	%residxtmp_65 = getelementptr i32*, i32** %tmp_63, i32 %tmp_64
	%tmp_66 = load i32*, i32** %residxtmp_65
	%tmp_67 = load i32, i32* %m2ColIdx19
	%residxtmp_68 = getelementptr i32, i32* %tmp_66, i32 %tmp_67
	%tmp_69 = load i32, i32* %residxtmp_68
	%tmp_70 = load i32**, i32*** %m15
	%tmp_71 = load i32, i32* %m1RowIdx12
	%m1idxtmp_72 = getelementptr i32*, i32** %tmp_70, i32 %tmp_71
	%tmp_73 = load i32*, i32** %m1idxtmp_72
	%tmp_74 = load i32, i32* %m2RowIdx26
	%m1idxtmp_75 = getelementptr i32, i32* %tmp_73, i32 %tmp_74
	%tmp_76 = load i32, i32* %m1idxtmp_75
	%tmp_77 = load i32**, i32*** %m26
	%tmp_78 = load i32, i32* %m2RowIdx26
	%m2idxtmp_79 = getelementptr i32*, i32** %tmp_77, i32 %tmp_78
	%tmp_80 = load i32*, i32** %m2idxtmp_79
	%tmp_81 = load i32, i32* %m2ColIdx19
	%m2idxtmp_82 = getelementptr i32, i32* %tmp_80, i32 %tmp_81
	%tmp_83 = load i32, i32* %m2idxtmp_82
	%tmp_84 = mul i32 %tmp_76, %tmp_83
	%tmp_85 = add i32 %tmp_69, %tmp_84
	store i32 %tmp_85, i32* %residxtmp_61
	%tmp_86 = load i32, i32* %m2RowIdx26
	%tmp_87 = add i32 %tmp_86, 1
	store i32 %tmp_87, i32* %m2RowIdx26
	br label %while_cond27
while_end29:
	%tmp_88 = load i32, i32* %m2ColIdx19
	%tmp_89 = add i32 %tmp_88, 1
	store i32 %tmp_89, i32* %m2ColIdx19
	br label %while_cond20
while_end22:
	%tmp_90 = load i32, i32* %m1RowIdx12
	%tmp_91 = add i32 %tmp_90, 1
	store i32 %tmp_91, i32* %m1RowIdx12
	br label %while_cond13
while_end15:
	%tmp_92 = load i32**, i32*** %res8
	store i32** %tmp_92, i32*** %matrixProduct7
	%tmp_93 = load i32**, i32*** %matrixProduct7
	ret i32** %tmp_93
}
define void @print_matrix(i32** %m, i32 %rows, i32 %cols) {
	%m94 = alloca i32**
	%rows95 = alloca i32
	%cols96 = alloca i32
	store i32** %m, i32*** %m94
	store i32 %rows, i32* %rows95
	store i32 %cols, i32* %cols96
	%i97 = alloca i32
	store i32 0, i32* %i97
	br label %while_cond98
while_cond98:
	%tmp_101 = load i32, i32* %i97
	%tmp_102 = load i32, i32* %rows95
	%tmp_103 = icmp slt i32 %tmp_101, %tmp_102
	br i1 %tmp_103, label %while_body99, label %while_end100
while_body99:
	%tmp_105 = alloca i8*
	store i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.pl_str_104, i64 0, i64 0), i8** %tmp_105
	%tmp_106 = load i8*, i8** %tmp_105
	call void @print_string( i8*  %tmp_106 )
	%tmp_107 = load i32, i32* %i97
	call void @print_int( i32  %tmp_107 )
	%tmp_109 = alloca i8*
	store i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.pl_str_108, i64 0, i64 0), i8** %tmp_109
	%tmp_110 = load i8*, i8** %tmp_109
	call void @print_string( i8*  %tmp_110 )
	%j111 = alloca i32
	store i32 0, i32* %j111
	br label %while_cond112
while_cond112:
	%tmp_115 = load i32, i32* %j111
	%tmp_116 = load i32, i32* %cols96
	%tmp_117 = icmp slt i32 %tmp_115, %tmp_116
	br i1 %tmp_117, label %while_body113, label %while_end114
while_body113:
	%tmp_118 = load i32**, i32*** %m94
	%tmp_119 = load i32, i32* %i97
	%midxtmp_120 = getelementptr i32*, i32** %tmp_118, i32 %tmp_119
	%tmp_121 = load i32*, i32** %midxtmp_120
	%tmp_122 = load i32, i32* %j111
	%midxtmp_123 = getelementptr i32, i32* %tmp_121, i32 %tmp_122
	%tmp_124 = load i32, i32* %midxtmp_123
	call void @print_int( i32  %tmp_124 )
	%tmp_125 = load i32, i32* %j111
	%tmp_126 = add i32 %tmp_125, 1
	store i32 %tmp_126, i32* %j111
	br label %while_cond112
while_end114:
	%tmp_127 = load i32, i32* %i97
	%tmp_128 = add i32 %tmp_127, 1
	store i32 %tmp_128, i32* %i97
	%tmp_129 = alloca i8*
	store i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.pl_str_108, i64 0, i64 0), i8** %tmp_129
	%tmp_130 = load i8*, i8** %tmp_129
	call void @print_string( i8*  %tmp_130 )
	br label %while_cond98
while_end100:
	ret void
}
define void @main() {
	%m1131 = alloca i32**
	%tmp_132 = load i32, i32* @m1_rows1
	%tmp_133 = load i32, i32* @m1_cols2
	%tmp_134 = call i32** @get_int_matrix( i32  %tmp_132, i32  %tmp_133 )
	store i32** %tmp_134, i32*** %m1131
	%m2135 = alloca i32**
	%tmp_136 = load i32, i32* @m2_rows3
	%tmp_137 = load i32, i32* @m2_cols4
	%tmp_138 = call i32** @get_int_matrix( i32  %tmp_136, i32  %tmp_137 )
	store i32** %tmp_138, i32*** %m2135
	%tmp_139 = load i32**, i32*** %m1131
	%tmp_140 = load i32**, i32*** %m2135
	%tmp_141 = call i32** @matrixProduct( i32**  %tmp_139, i32**  %tmp_140 )
	%tmp_142 = load i32, i32* @m1_rows1
	%tmp_143 = load i32, i32* @m2_cols4
	call void @print_matrix( i32**  %tmp_141, i32  %tmp_142, i32  %tmp_143 )
	ret void
}