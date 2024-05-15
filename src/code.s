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
	movq	x1(%rip), %rdi
	callq	print_string@PLT
	popq	%rax
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end0:
	.size	main, .Lfunc_end0-main
	.cfi_endproc
                                        # -- End function
	.type	.L.pl_str_2,@object             # @.pl_str_2
	.section	.rodata.str1.1,"aMS",@progbits,1
.L.pl_str_2:
	.asciz	"Test"
	.size	.L.pl_str_2, 5

	.type	x1,@object                      # @x1
	.data
	.globl	x1
	.p2align	3
x1:
	.quad	.L.pl_str_2
	.size	x1, 8

	.section	".note.GNU-stack","",@progbits
