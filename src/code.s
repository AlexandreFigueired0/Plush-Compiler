	.text
	.file	"code.ll"
	.globl	matrixProduct                   # -- Begin function matrixProduct
	.p2align	4, 0x90
	.type	matrixProduct,@function
matrixProduct:                          # @matrixProduct
	.cfi_startproc
# %bb.0:
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	subq	$48, %rsp
	movq	%rdi, -32(%rbp)
	movq	%rsi, -24(%rbp)
	movl	m1_rows1(%rip), %edi
	movl	m2_cols4(%rip), %esi
	callq	get_int_matrix@PLT
	movq	%rax, -16(%rbp)
	movl	$0, -4(%rbp)
	jmp	.LBB0_1
	.p2align	4, 0x90
.LBB0_8:                                # %while_end22
                                        #   in Loop: Header=BB0_1 Depth=1
	incl	-4(%rbp)
.LBB0_1:                                # %while_cond13
                                        # =>This Loop Header: Depth=1
                                        #     Child Loop BB0_3 Depth 2
                                        #       Child Loop BB0_5 Depth 3
	movl	-4(%rbp), %eax
	cmpl	m1_rows1(%rip), %eax
	jge	.LBB0_9
# %bb.2:                                # %while_body14
                                        #   in Loop: Header=BB0_1 Depth=1
	movq	%rsp, %rcx
	leaq	-16(%rcx), %rax
	movq	%rax, %rsp
	movl	$0, -16(%rcx)
	jmp	.LBB0_3
	.p2align	4, 0x90
.LBB0_7:                                # %while_end29
                                        #   in Loop: Header=BB0_3 Depth=2
	incl	(%rax)
.LBB0_3:                                # %while_cond20
                                        #   Parent Loop BB0_1 Depth=1
                                        # =>  This Loop Header: Depth=2
                                        #       Child Loop BB0_5 Depth 3
	movl	(%rax), %ecx
	cmpl	m2_rows3(%rip), %ecx
	jge	.LBB0_8
# %bb.4:                                # %while_body21
                                        #   in Loop: Header=BB0_3 Depth=2
	movq	%rsp, %rdx
	leaq	-16(%rdx), %rcx
	movq	%rcx, %rsp
	movl	$0, -16(%rdx)
	.p2align	4, 0x90
.LBB0_5:                                # %while_cond27
                                        #   Parent Loop BB0_1 Depth=1
                                        #     Parent Loop BB0_3 Depth=2
                                        # =>    This Inner Loop Header: Depth=3
	movl	(%rcx), %edx
	cmpl	m2_rows3(%rip), %edx
	jge	.LBB0_7
# %bb.6:                                # %while_body28
                                        #   in Loop: Header=BB0_5 Depth=3
	incl	(%rcx)
	jmp	.LBB0_5
.LBB0_9:                                # %while_end15
	movq	-16(%rbp), %rax
	movq	%rax, -40(%rbp)
	movq	%rbp, %rsp
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end0:
	.size	matrixProduct, .Lfunc_end0-matrixProduct
	.cfi_endproc
                                        # -- End function
	.globl	print_matrix                    # -- Begin function print_matrix
	.p2align	4, 0x90
	.type	print_matrix,@function
print_matrix:                           # @print_matrix
	.cfi_startproc
# %bb.0:
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%rbx
	subq	$24, %rsp
	.cfi_offset %rbx, -24
	movq	%rdi, -32(%rbp)
	movl	%esi, -20(%rbp)
	movl	%edx, -16(%rbp)
	movl	$0, -12(%rbp)
	jmp	.LBB1_1
	.p2align	4, 0x90
.LBB1_5:                                # %while_end61
                                        #   in Loop: Header=BB1_1 Depth=1
	incl	-12(%rbp)
	movq	%rsp, %rax
	leaq	-16(%rax), %rsp
	movq	$.L.pl_str_55, -16(%rax)
	movl	$.L.pl_str_55, %edi
	callq	print_string@PLT
.LBB1_1:                                # %while_cond45
                                        # =>This Loop Header: Depth=1
                                        #     Child Loop BB1_3 Depth 2
	movl	-12(%rbp), %eax
	cmpl	-20(%rbp), %eax
	jge	.LBB1_6
# %bb.2:                                # %while_body46
                                        #   in Loop: Header=BB1_1 Depth=1
	movq	%rsp, %rax
	leaq	-16(%rax), %rsp
	movq	$.L.pl_str_51, -16(%rax)
	movl	$.L.pl_str_51, %edi
	callq	print_string@PLT
	movl	-12(%rbp), %edi
	callq	print_int@PLT
	movq	%rsp, %rax
	leaq	-16(%rax), %rsp
	movq	$.L.pl_str_55, -16(%rax)
	movl	$.L.pl_str_55, %edi
	callq	print_string@PLT
	movq	%rsp, %rax
	leaq	-16(%rax), %rbx
	movq	%rbx, %rsp
	movl	$0, -16(%rax)
	.p2align	4, 0x90
.LBB1_3:                                # %while_cond59
                                        #   Parent Loop BB1_1 Depth=1
                                        # =>  This Inner Loop Header: Depth=2
	movl	(%rbx), %eax
	cmpl	-16(%rbp), %eax
	jge	.LBB1_5
# %bb.4:                                # %while_body60
                                        #   in Loop: Header=BB1_3 Depth=2
	movq	-32(%rbp), %rax
	movslq	-12(%rbp), %rcx
	movq	(%rax,%rcx,8), %rax
	movslq	(%rbx), %rcx
	movl	(%rax,%rcx,4), %edi
	callq	print_int@PLT
	incl	(%rbx)
	jmp	.LBB1_3
.LBB1_6:                                # %while_end47
	leaq	-8(%rbp), %rsp
	popq	%rbx
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end1:
	.size	print_matrix, .Lfunc_end1-print_matrix
	.cfi_endproc
                                        # -- End function
	.globl	main                            # -- Begin function main
	.p2align	4, 0x90
	.type	main,@function
main:                                   # @main
	.cfi_startproc
# %bb.0:
	subq	$24, %rsp
	.cfi_def_cfa_offset 32
	movl	m1_rows1(%rip), %edi
	movl	m1_cols2(%rip), %esi
	callq	get_int_matrix@PLT
	movq	%rax, 8(%rsp)
	movl	m2_rows3(%rip), %edi
	movl	m2_cols4(%rip), %esi
	callq	get_int_matrix@PLT
	movq	%rax, 16(%rsp)
	movq	8(%rsp), %rdi
	movq	%rax, %rsi
	callq	matrixProduct@PLT
	movl	m1_rows1(%rip), %esi
	movl	m2_cols4(%rip), %edx
	movq	%rax, %rdi
	callq	print_matrix@PLT
	addq	$24, %rsp
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end2:
	.size	main, .Lfunc_end2-main
	.cfi_endproc
                                        # -- End function
	.type	.L.pl_str_55,@object            # @.pl_str_55
	.section	.rodata.str1.1,"aMS",@progbits,1
.L.pl_str_55:
	.asciz	"--"
	.size	.L.pl_str_55, 3

	.type	.L.pl_str_51,@object            # @.pl_str_51
.L.pl_str_51:
	.asciz	"row"
	.size	.L.pl_str_51, 4

	.type	m1_rows1,@object                # @m1_rows1
	.data
	.globl	m1_rows1
	.p2align	2
m1_rows1:
	.long	3                               # 0x3
	.size	m1_rows1, 4

	.type	m1_cols2,@object                # @m1_cols2
	.globl	m1_cols2
	.p2align	2
m1_cols2:
	.long	2                               # 0x2
	.size	m1_cols2, 4

	.type	m2_rows3,@object                # @m2_rows3
	.globl	m2_rows3
	.p2align	2
m2_rows3:
	.long	2                               # 0x2
	.size	m2_rows3, 4

	.type	m2_cols4,@object                # @m2_cols4
	.globl	m2_cols4
	.p2align	2
m2_cols4:
	.long	2                               # 0x2
	.size	m2_cols4, 4

	.section	".note.GNU-stack","",@progbits
