	.text
	.file	"code.ll"
	.globl	main                            # -- Begin function main
	.p2align	4, 0x90
	.type	main,@function
main:                                   # @main
	.cfi_startproc
# %bb.0:
	pushq	%rax
	.cfi_def_cfa_offset 16
	movl	$-1, 4(%rsp)
	cmpl	$4, 4(%rsp)
	jg	.LBB0_3
	.p2align	4, 0x90
.LBB0_2:                                # %while_body4
                                        # =>This Inner Loop Header: Depth=1
	movl	4(%rsp), %edi
	callq	print_int@PLT
	incl	4(%rsp)
	cmpl	$4, 4(%rsp)
	jle	.LBB0_2
.LBB0_3:                                # %while_end5
	movl	4(%rsp), %edi
	callq	print_int@PLT
	movl	4(%rsp), %edi
	movl	$2, %esi
	callq	mult@PLT
	movl	%eax, %edi
	callq	print_int@PLT
	popq	%rax
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end0:
	.size	main, .Lfunc_end0-main
	.cfi_endproc
                                        # -- End function
	.globl	mult                            # -- Begin function mult
	.p2align	4, 0x90
	.type	mult,@function
mult:                                   # @mult
	.cfi_startproc
# %bb.0:
	movl	%edi, %eax
	movl	%edi, -8(%rsp)
	movl	%esi, -12(%rsp)
	imull	%esi, %eax
	movl	%eax, -4(%rsp)
	retq
.Lfunc_end1:
	.size	mult, .Lfunc_end1-mult
	.cfi_endproc
                                        # -- End function
	.section	".note.GNU-stack","",@progbits
