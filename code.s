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
	callq	hello@PLT
	popq	%rax
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end0:
	.size	main, .Lfunc_end0-main
	.cfi_endproc
                                        # -- End function
	.globl	hello                           # -- Begin function hello
	.p2align	4, 0x90
	.type	hello,@function
hello:                                  # @hello
	.cfi_startproc
# %bb.0:
	pushq	%rax
	.cfi_def_cfa_offset 16
	movq	$.L.pl_str_1, (%rsp)
	movl	$.L.pl_str_1, %edi
	callq	print_string@PLT
	popq	%rax
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end1:
	.size	hello, .Lfunc_end1-hello
	.cfi_endproc
                                        # -- End function
	.type	.L.pl_str_1,@object             # @.pl_str_1
	.section	.rodata.str1.1,"aMS",@progbits,1
.L.pl_str_1:
	.asciz	"Hello, World!"
	.size	.L.pl_str_1, 14

	.section	".note.GNU-stack","",@progbits
