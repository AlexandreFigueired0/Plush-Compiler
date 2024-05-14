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
	movq	$.L.pl_str_3, (%rsp)
	movl	$.L.pl_str_3, %edi
	callq	print_string@PLT
	popq	%rax
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end0:
	.size	main, .Lfunc_end0-main
	.cfi_endproc
                                        # -- End function
	.type	.L.pl_str_3,@object             # @.pl_str_3
	.section	.rodata.str1.1,"aMS",@progbits,1
.L.pl_str_3:
	.asciz	"Bye"
	.size	.L.pl_str_3, 4

	.type	.L.pl_str_2,@object             # @.pl_str_2
.L.pl_str_2:
	.asciz	"Hello World!"
	.size	.L.pl_str_2, 13

	.section	".note.GNU-stack","",@progbits
