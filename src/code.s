	.text
	.file	"code.ll"
	.globl	maxRangeSquared                 # -- Begin function maxRangeSquared
	.p2align	4, 0x90
	.type	maxRangeSquared,@function
maxRangeSquared:                        # @maxRangeSquared
	.cfi_startproc
# %bb.0:
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r14
	pushq	%rbx
	subq	$16, %rsp
	.cfi_offset %rbx, -32
	.cfi_offset %r14, -24
	movl	%edi, -24(%rbp)
	movl	%esi, -28(%rbp)
	movl	$2, %esi
	callq	power_int@PLT
	movl	%eax, -20(%rbp)
	jmp	.LBB0_1
	.p2align	4, 0x90
.LBB0_4:                                # %if_end23
                                        #   in Loop: Header=BB0_1 Depth=1
	incl	-24(%rbp)
.LBB0_1:                                # %while_cond10
                                        # =>This Inner Loop Header: Depth=1
	movl	-24(%rbp), %eax
	cmpl	-28(%rbp), %eax
	jg	.LBB0_5
# %bb.2:                                # %while_body11
                                        #   in Loop: Header=BB0_1 Depth=1
	movq	%rsp, %rbx
	leaq	-16(%rbx), %r14
	movq	%r14, %rsp
	movl	-24(%rbp), %edi
	movl	$2, %esi
	callq	power_int@PLT
	movl	%eax, -16(%rbx)
	cmpl	-20(%rbp), %eax
	jle	.LBB0_4
# %bb.3:                                # %if_true22
                                        #   in Loop: Header=BB0_1 Depth=1
	movl	(%r14), %eax
	movl	%eax, -20(%rbp)
	jmp	.LBB0_4
.LBB0_5:                                # %while_end12
	movl	-20(%rbp), %eax
	movl	%eax, -32(%rbp)
	leaq	-16(%rbp), %rsp
	popq	%rbx
	popq	%r14
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end0:
	.size	maxRangeSquared, .Lfunc_end0-maxRangeSquared
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
	movq	%rdi, 16(%rsp)
	movl	actual_min1(%rip), %edi
	movl	actual_max3(%rip), %esi
	callq	maxRangeSquared@PLT
	movl	%eax, 12(%rsp)
	movl	%eax, %edi
	callq	print_int@PLT
	addq	$24, %rsp
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end1:
	.size	main, .Lfunc_end1-main
	.cfi_endproc
                                        # -- End function
	.type	actual_min1,@object             # @actual_min1
	.data
	.globl	actual_min1
	.p2align	2
actual_min1:
	.long	4294967287                      # 0xfffffff7
	.size	actual_min1, 4

	.type	actual_max3,@object             # @actual_max3
	.globl	actual_max3
	.p2align	2
actual_max3:
	.long	9                               # 0x9
	.size	actual_max3, 4

	.section	".note.GNU-stack","",@progbits
