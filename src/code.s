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
	leaq	-16(%rcx), %r8
	movq	%r8, %rsp
	movl	$0, -16(%rcx)
	jmp	.LBB0_3
	.p2align	4, 0x90
.LBB0_7:                                # %while_end29
                                        #   in Loop: Header=BB0_3 Depth=2
	incl	(%r8)
.LBB0_3:                                # %while_cond20
                                        #   Parent Loop BB0_1 Depth=1
                                        # =>  This Loop Header: Depth=2
                                        #       Child Loop BB0_5 Depth 3
	movl	(%r8), %ecx
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
	movq	-16(%rbp), %rdx
	movslq	-4(%rbp), %rsi
	movq	(%rdx,%rsi,8), %r9
	movslq	(%r8), %rdi
	movq	-32(%rbp), %rax
	movq	(%rax,%rsi,8), %rax
	movslq	(%rcx), %rsi
	movl	(%rax,%rsi,4), %eax
	movq	-24(%rbp), %rdx
	movq	(%rdx,%rsi,8), %rdx
	imull	(%rdx,%rdi,4), %eax
	addl	%eax, (%r9,%rdi,4)
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
	subq	$24, %rsp
	.cfi_def_cfa_offset 32
	movq	%rdi, 16(%rsp)
	movl	%esi, 12(%rsp)
	movl	%edx, 8(%rsp)
	movl	$0, 4(%rsp)
	.p2align	4, 0x90
.LBB1_1:                                # %while_cond75
                                        # =>This Inner Loop Header: Depth=1
	movl	4(%rsp), %eax
	cmpl	12(%rsp), %eax
	jge	.LBB1_3
# %bb.2:                                # %while_body76
                                        #   in Loop: Header=BB1_1 Depth=1
	movq	16(%rsp), %rax
	movslq	4(%rsp), %rcx
	movq	(%rax,%rcx,8), %rdi
	movl	8(%rsp), %esi
	callq	print_int_array@PLT
	incl	4(%rsp)
	jmp	.LBB1_1
.LBB1_3:                                # %while_end77
	addq	$24, %rsp
	.cfi_def_cfa_offset 8
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
	movq	8(%rsp), %rax
	movq	(%rax), %rax
	movl	$1, (%rax)
	movq	8(%rsp), %rax
	movq	(%rax), %rax
	movl	$2, 4(%rax)
	movq	8(%rsp), %rax
	movq	8(%rax), %rax
	movl	$3, (%rax)
	movq	8(%rsp), %rax
	movq	8(%rax), %rax
	movl	$4, 4(%rax)
	movq	8(%rsp), %rax
	movq	16(%rax), %rax
	movl	$5, (%rax)
	movq	8(%rsp), %rax
	movq	16(%rax), %rax
	movl	$6, 4(%rax)
	movq	16(%rsp), %rax
	movq	(%rax), %rax
	movl	$1, (%rax)
	movq	16(%rsp), %rax
	movq	(%rax), %rax
	movl	$2, 4(%rax)
	movq	16(%rsp), %rax
	movq	8(%rax), %rax
	movl	$3, (%rax)
	movq	16(%rsp), %rax
	movq	8(%rax), %rax
	movl	$4, 4(%rax)
	movq	8(%rsp), %rdi
	movq	16(%rsp), %rsi
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
