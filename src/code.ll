@m1_rows1 = dso_local global i32 3
@m1_cols2 = dso_local global i32 2
@m2_rows3 = dso_local global i32 2
@m2_cols4 = dso_local global i32 2
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
define i32** @matrixProduct(i32** %m1, i32** %m2) {
	%matrixProduct7 = alloca i32**
	%m15 = alloca i32**
	%m26 = alloca i32**
	store i32** %m1, i32*** %m15
	store i32** %m2, i32*** %m26
	%res8 = alloca i32**
	%tmp_9 = load i32, i32* @m1_rows1
	%tmp_10 = load i32, i32* @m2_cols4
	%get_int_matrix_11 = call i32** @get_int_matrix( i32  %tmp_9, i32  %tmp_10 )
	store i32** %get_int_matrix_11, i32*** %res8
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
	%res_idx_35 = getelementptr i32*, i32** %tmp_33, i32 %tmp_34
	%tmp_36 = load i32*, i32** %res_idx_35
	%tmp_37 = load i32, i32* %m2ColIdx19
	%res_idx_38 = getelementptr i32, i32* %tmp_36, i32 %tmp_37
	%tmp_39 = load i32, i32* %res_idx_38
	%tmp_40 = load i32**, i32*** %res8
	%tmp_41 = load i32, i32* %m1RowIdx12
	%res_idx_42 = getelementptr i32*, i32** %tmp_40, i32 %tmp_41
	%tmp_43 = load i32*, i32** %res_idx_42
	%tmp_44 = load i32, i32* %m2ColIdx19
	%res_idx_45 = getelementptr i32, i32* %tmp_43, i32 %tmp_44
	%tmp_46 = load i32, i32* %res_idx_45
	%tmp_47 = load i32**, i32*** %m15
	%tmp_48 = load i32, i32* %m1RowIdx12
	%m1_idx_49 = getelementptr i32*, i32** %tmp_47, i32 %tmp_48
	%tmp_50 = load i32*, i32** %m1_idx_49
	%tmp_51 = load i32, i32* %m2RowIdx26
	%m1_idx_52 = getelementptr i32, i32* %tmp_50, i32 %tmp_51
	%tmp_53 = load i32, i32* %m1_idx_52
	%tmp_54 = load i32**, i32*** %m26
	%tmp_55 = load i32, i32* %m2RowIdx26
	%m2_idx_56 = getelementptr i32*, i32** %tmp_54, i32 %tmp_55
	%tmp_57 = load i32*, i32** %m2_idx_56
	%tmp_58 = load i32, i32* %m2ColIdx19
	%m2_idx_59 = getelementptr i32, i32* %tmp_57, i32 %tmp_58
	%tmp_60 = load i32, i32* %m2_idx_59
	%tmp_61 = mul i32 %tmp_53, %tmp_60
	%tmp_62 = add i32 %tmp_46, %tmp_61
	store i32 %tmp_62, i32* %res_idx_38
	%tmp_63 = load i32, i32* %m2RowIdx26
	%tmp_64 = add i32 %tmp_63, 1
	store i32 %tmp_64, i32* %m2RowIdx26
	br label %while_cond27
while_end29:
	%tmp_65 = load i32, i32* %m2ColIdx19
	%tmp_66 = add i32 %tmp_65, 1
	store i32 %tmp_66, i32* %m2ColIdx19
	br label %while_cond20
while_end22:
	%tmp_67 = load i32, i32* %m1RowIdx12
	%tmp_68 = add i32 %tmp_67, 1
	store i32 %tmp_68, i32* %m1RowIdx12
	br label %while_cond13
while_end15:
	%tmp_69 = load i32**, i32*** %res8
	store i32** %tmp_69, i32*** %matrixProduct7
	%tmp_70 = load i32**, i32*** %matrixProduct7
	ret i32** %tmp_70
}
define void @print_matrix(i32** %m, i32 %rows, i32 %cols) {
	%m71 = alloca i32**
	%rows72 = alloca i32
	%cols73 = alloca i32
	store i32** %m, i32*** %m71
	store i32 %rows, i32* %rows72
	store i32 %cols, i32* %cols73
	%i74 = alloca i32
	store i32 0, i32* %i74
	br label %while_cond75
while_cond75:
	%tmp_78 = load i32, i32* %i74
	%tmp_79 = load i32, i32* %rows72
	%tmp_80 = icmp slt i32 %tmp_78, %tmp_79
	br i1 %tmp_80, label %while_body76, label %while_end77
while_body76:
	%tmp_81 = load i32**, i32*** %m71
	%tmp_82 = load i32, i32* %i74
	%m_idx_83 = getelementptr i32*, i32** %tmp_81, i32 %tmp_82
	%tmp_84 = load i32*, i32** %m_idx_83
	%tmp_85 = load i32, i32* %cols73
	call void @print_int_array( i32*  %tmp_84, i32  %tmp_85 )
	%tmp_86 = load i32, i32* %i74
	%tmp_87 = add i32 %tmp_86, 1
	store i32 %tmp_87, i32* %i74
	br label %while_cond75
while_end77:
	ret void
}
define void @main() {
	%m188 = alloca i32**
	%tmp_89 = load i32, i32* @m1_rows1
	%tmp_90 = load i32, i32* @m1_cols2
	%get_int_matrix_91 = call i32** @get_int_matrix( i32  %tmp_89, i32  %tmp_90 )
	store i32** %get_int_matrix_91, i32*** %m188
	%m292 = alloca i32**
	%tmp_93 = load i32, i32* @m2_rows3
	%tmp_94 = load i32, i32* @m2_cols4
	%get_int_matrix_95 = call i32** @get_int_matrix( i32  %tmp_93, i32  %tmp_94 )
	store i32** %get_int_matrix_95, i32*** %m292
	%tmp_96 = load i32**, i32*** %m188
	%m1_idx_97 = getelementptr i32*, i32** %tmp_96, i32 0
	%tmp_98 = load i32*, i32** %m1_idx_97
	%m1_idx_99 = getelementptr i32, i32* %tmp_98, i32 0
	%tmp_100 = load i32, i32* %m1_idx_99
	store i32 1, i32* %m1_idx_99
	%tmp_101 = load i32**, i32*** %m188
	%m1_idx_102 = getelementptr i32*, i32** %tmp_101, i32 0
	%tmp_103 = load i32*, i32** %m1_idx_102
	%m1_idx_104 = getelementptr i32, i32* %tmp_103, i32 1
	%tmp_105 = load i32, i32* %m1_idx_104
	store i32 2, i32* %m1_idx_104
	%tmp_106 = load i32**, i32*** %m188
	%m1_idx_107 = getelementptr i32*, i32** %tmp_106, i32 1
	%tmp_108 = load i32*, i32** %m1_idx_107
	%m1_idx_109 = getelementptr i32, i32* %tmp_108, i32 0
	%tmp_110 = load i32, i32* %m1_idx_109
	store i32 3, i32* %m1_idx_109
	%tmp_111 = load i32**, i32*** %m188
	%m1_idx_112 = getelementptr i32*, i32** %tmp_111, i32 1
	%tmp_113 = load i32*, i32** %m1_idx_112
	%m1_idx_114 = getelementptr i32, i32* %tmp_113, i32 1
	%tmp_115 = load i32, i32* %m1_idx_114
	store i32 4, i32* %m1_idx_114
	%tmp_116 = load i32**, i32*** %m188
	%m1_idx_117 = getelementptr i32*, i32** %tmp_116, i32 2
	%tmp_118 = load i32*, i32** %m1_idx_117
	%m1_idx_119 = getelementptr i32, i32* %tmp_118, i32 0
	%tmp_120 = load i32, i32* %m1_idx_119
	store i32 5, i32* %m1_idx_119
	%tmp_121 = load i32**, i32*** %m188
	%m1_idx_122 = getelementptr i32*, i32** %tmp_121, i32 2
	%tmp_123 = load i32*, i32** %m1_idx_122
	%m1_idx_124 = getelementptr i32, i32* %tmp_123, i32 1
	%tmp_125 = load i32, i32* %m1_idx_124
	store i32 6, i32* %m1_idx_124
	%tmp_126 = load i32**, i32*** %m292
	%m2_idx_127 = getelementptr i32*, i32** %tmp_126, i32 0
	%tmp_128 = load i32*, i32** %m2_idx_127
	%m2_idx_129 = getelementptr i32, i32* %tmp_128, i32 0
	%tmp_130 = load i32, i32* %m2_idx_129
	store i32 1, i32* %m2_idx_129
	%tmp_131 = load i32**, i32*** %m292
	%m2_idx_132 = getelementptr i32*, i32** %tmp_131, i32 0
	%tmp_133 = load i32*, i32** %m2_idx_132
	%m2_idx_134 = getelementptr i32, i32* %tmp_133, i32 1
	%tmp_135 = load i32, i32* %m2_idx_134
	store i32 2, i32* %m2_idx_134
	%tmp_136 = load i32**, i32*** %m292
	%m2_idx_137 = getelementptr i32*, i32** %tmp_136, i32 1
	%tmp_138 = load i32*, i32** %m2_idx_137
	%m2_idx_139 = getelementptr i32, i32* %tmp_138, i32 0
	%tmp_140 = load i32, i32* %m2_idx_139
	store i32 3, i32* %m2_idx_139
	%tmp_141 = load i32**, i32*** %m292
	%m2_idx_142 = getelementptr i32*, i32** %tmp_141, i32 1
	%tmp_143 = load i32*, i32** %m2_idx_142
	%m2_idx_144 = getelementptr i32, i32* %tmp_143, i32 1
	%tmp_145 = load i32, i32* %m2_idx_144
	store i32 4, i32* %m2_idx_144
	%tmp_146 = load i32**, i32*** %m188
	%tmp_147 = load i32**, i32*** %m292
	%matrixProduct_148 = call i32** @matrixProduct( i32**  %tmp_146, i32**  %tmp_147 )
	%tmp_149 = load i32, i32* @m1_rows1
	%tmp_150 = load i32, i32* @m2_cols4
	call void @print_matrix( i32**  %matrixProduct_148, i32  %tmp_149, i32  %tmp_150 )
	ret void
}