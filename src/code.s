	.text
	.file	"code.ll"
	.globl	print_int                       # -- Begin function print_int
	.p2align	4, 0x90
	.type	print_int,@function
print_int:                              # @print_int
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rax
	.cfi_def_cfa_offset 16
	movl	%edi, %esi
	movl	%edi, 4(%rsp)
	movl	$.L.str, %edi
	xorl	%eax, %eax
	callq	printf@PLT
	popq	%rax
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end0:
	.size	print_int, .Lfunc_end0-print_int
	.cfi_endproc
                                        # -- End function
	.globl	main                            # -- Begin function main
	.p2align	4, 0x90
	.type	main,@function
main:                                   # @main
	.cfi_startproc
# %bb.0:
	pushq	%rax
	.cfi_def_cfa_offset 16
	movl	$-1, 4(%rsp)
	cmpl	$4, 4(%rsp)
	jg	.LBB1_3
	.p2align	4, 0x90
.LBB1_2:                                # %while_body4
                                        # =>This Inner Loop Header: Depth=1
	movl	4(%rsp), %edi
	callq	print_int@PLT
	incl	4(%rsp)
	cmpl	$4, 4(%rsp)
	jle	.LBB1_2
.LBB1_3:                                # %while_end5
	movl	4(%rsp), %edi
	callq	print_int@PLT
	popq	%rax
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end1:
	.size	main, .Lfunc_end1-main
	.cfi_endproc
                                        # -- End function
	.type	.L.str,@object                  # @.str
	.section	.rodata.str1.1,"aMS",@progbits,1
.L.str:
	.asciz	"%d\n"
	.size	.L.str, 4

	.section	".note.GNU-stack","",@progbits
