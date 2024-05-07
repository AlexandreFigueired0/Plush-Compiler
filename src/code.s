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
	movl	$2, 4(%rsp)
	movb	$1, %al
	testb	%al, %al
	jne	.LBB0_2
# %bb.1:                                # %if_true5
	movl	$1, 4(%rsp)
.LBB0_2:                                # %if_end6
	movl	4(%rsp), %esi
	movl	$.L.plush_str_tmp_7, %edi
	xorl	%eax, %eax
	callq	printf@PLT
	popq	%rax
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end0:
	.size	main, .Lfunc_end0-main
	.cfi_endproc
                                        # -- End function
	.type	.L.plush_str_tmp_7,@object      # @.plush_str_tmp_7
	.section	.rodata,"a",@progbits
.L.plush_str_tmp_7:
	.asciz	"%d\n"
	.size	.L.plush_str_tmp_7, 4

	.section	".note.GNU-stack","",@progbits
