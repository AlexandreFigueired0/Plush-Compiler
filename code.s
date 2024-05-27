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
	movq	$.L.pl_str_2, 16(%rsp)
	movl	$.L.pl_str_2, %edi
	callq	string_to_char_array@PLT
	movq	%rax, 8(%rsp)
	movzbl	(%rax), %edi
	callq	print_char@PLT
	addq	$24, %rsp
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end0:
	.size	main, .Lfunc_end0-main
	.cfi_endproc
                                        # -- End function
	.type	.L.pl_str_2,@object             # @.pl_str_2
	.section	.rodata.str1.1,"aMS",@progbits,1
.L.pl_str_2:
	.asciz	"test"
	.size	.L.pl_str_2, 5

	.section	".note.GNU-stack","",@progbits
