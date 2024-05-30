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
	.globl	hello_world                     # -- Begin function hello_world
	.p2align	4, 0x90
	.type	hello_world,@function
hello_world:                            # @hello_world
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
	.size	hello_world, .Lfunc_end1-hello_world
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
	callq	hello_world@PLT
	popq	%rax
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end2:
	.size	hello, .Lfunc_end2-hello
	.cfi_endproc
                                        # -- End function
	.type	.L.pl_str_1,@object             # @.pl_str_1
	.section	.rodata.str1.1,"aMS",@progbits,1
.L.pl_str_1:
	.asciz	"Hello, World!\\n"
	.size	.L.pl_str_1, 16

	.section	".note.GNU-stack","",@progbits
