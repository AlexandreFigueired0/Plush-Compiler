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
	movl	$3, %edi
	movl	$3, %esi
	callq	get_string_matrix@PLT
	movq	%rax, (%rsp)
	movq	(%rax), %rax
	movq	$.L.pl_str_8, (%rax)
	popq	%rax
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end0:
	.size	main, .Lfunc_end0-main
	.cfi_endproc
                                        # -- End function
	.type	.L.pl_str_8,@object             # @.pl_str_8
	.section	.rodata.str1.1,"aMS",@progbits,1
.L.pl_str_8:
	.asciz	"Hello"
	.size	.L.pl_str_8, 6

	.section	".note.GNU-stack","",@progbits
