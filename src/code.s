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
	movl	$11, 4(%rsp)
	movl	$.L.plush_str_cas_1, %edi
	movl	$11, %esi
	xorl	%eax, %eax
	callq	printf@PLT
	popq	%rax
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end0:
	.size	main, .Lfunc_end0-main
	.cfi_endproc
                                        # -- End function
	.type	.L.plush_str_cas_1,@object      # @.plush_str_cas_1
	.section	.rodata,"a",@progbits
.L.plush_str_cas_1:
	.asciz	"%d\n"
	.size	.L.plush_str_cas_1, 4

	.section	".note.GNU-stack","",@progbits
