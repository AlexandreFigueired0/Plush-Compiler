	.text
	.file	"code.ll"
	.globl	main                            # -- Begin function main
	.p2align	4, 0x90
	.type	main,@function
main:                                   # @main
	.cfi_startproc
# %bb.0:
	subq	$24, %rsp
	.cfi_def_cfa_offset 32
	movl	$5, %edi
	callq	get_int_array@PLT
	movq	%rax, 8(%rsp)
	movl	$10, (%rax)
	movq	8(%rsp), %rax
	movl	(%rax), %edi
	movl	%edi, 20(%rsp)
	callq	print_int@PLT
	addq	$24, %rsp
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
	.globl	a                               # -- Begin function a
	.p2align	4, 0x90
	.type	a,@function
a:                                      # @a
	.cfi_startproc
# %bb.0:
	subq	$24, %rsp
	.cfi_def_cfa_offset 32
	movl	$5, %edi
	callq	get_int_array@PLT
	movq	%rax, 8(%rsp)
	movq	%rax, 16(%rsp)
	addq	$24, %rsp
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end2:
	.size	a, .Lfunc_end2-a
	.cfi_endproc
                                        # -- End function
	.section	".note.GNU-stack","",@progbits
