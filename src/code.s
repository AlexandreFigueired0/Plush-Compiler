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
	movq	$.Lpl_str_3, 8(%rsp)
	movq	$.Lpl_str_2, 16(%rsp)
	movl	$.Lpl_str_2, %edi
	callq	print_string@PLT
	movq	8(%rsp), %rdi
	callq	print_string@PLT
	addq	$24, %rsp
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end0:
	.size	main, .Lfunc_end0-main
	.cfi_endproc
                                        # -- End function
	.type	.Lpl_str_3,@object              # @pl_str_3
	.section	.rodata.str1.1,"aMS",@progbits,1
.Lpl_str_3:
	.asciz	"Bye"
	.size	.Lpl_str_3, 4

	.type	.Lpl_str_2,@object              # @pl_str_2
.Lpl_str_2:
	.asciz	"Hello World!"
	.size	.Lpl_str_2, 13

	.section	".note.GNU-stack","",@progbits
