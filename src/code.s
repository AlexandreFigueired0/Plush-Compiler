	.text
	.file	"code.ll"
	.globl	isPerfectSquare                 # -- Begin function isPerfectSquare
	.p2align	4, 0x90
	.type	isPerfectSquare,@function
isPerfectSquare:                        # @isPerfectSquare
	.cfi_startproc
# %bb.0:
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	subq	$32, %rsp
	movl	%edi, -16(%rbp)
	movb	$0, -1(%rbp)
	movl	$1, -12(%rbp)
	movl	%edi, -8(%rbp)
	.p2align	4, 0x90
.LBB0_1:                                # %while_cond8
                                        # =>This Inner Loop Header: Depth=1
	movl	-12(%rbp), %eax
	cmpl	-8(%rbp), %eax
	jg	.LBB0_11
# %bb.2:                                # %while_cond8
                                        #   in Loop: Header=BB0_1 Depth=1
	testb	$1, -1(%rbp)
	jne	.LBB0_11
# %bb.3:                                # %while_body9
                                        #   in Loop: Header=BB0_1 Depth=1
	movq	%rsp, %rdx
	leaq	-16(%rdx), %rax
	movq	%rax, %rsp
	movl	-12(%rbp), %ecx
	movl	-8(%rbp), %esi
	subl	%ecx, %esi
	movl	%esi, %edi
	shrl	$31, %edi
	addl	%esi, %edi
	sarl	%edi
	addl	%ecx, %edi
	movl	%edi, -16(%rdx)
	movq	%rsp, %rsi
	leaq	-16(%rsi), %rcx
	movq	%rcx, %rsp
	movl	-16(%rdx), %edx
	imull	%edx, %edx
	movl	%edx, -16(%rsi)
	cmpl	-16(%rbp), %edx
	jne	.LBB0_5
# %bb.4:                                # %if_true31
                                        #   in Loop: Header=BB0_1 Depth=1
	movb	$1, -1(%rbp)
.LBB0_5:                                # %if_end32
                                        #   in Loop: Header=BB0_1 Depth=1
	movl	-16(%rbp), %edx
	cmpl	%edx, (%rcx)
	je	.LBB0_8
# %bb.6:                                # %if_end32
                                        #   in Loop: Header=BB0_1 Depth=1
	jge	.LBB0_8
# %bb.7:                                # %if_true40
                                        #   in Loop: Header=BB0_1 Depth=1
	movl	(%rax), %edx
	incl	%edx
	movl	%edx, -12(%rbp)
.LBB0_8:                                # %if_end41
                                        #   in Loop: Header=BB0_1 Depth=1
	movl	-16(%rbp), %edx
	cmpl	%edx, (%rcx)
	je	.LBB0_1
# %bb.9:                                # %if_end41
                                        #   in Loop: Header=BB0_1 Depth=1
	jl	.LBB0_1
# %bb.10:                               # %if_true52
                                        #   in Loop: Header=BB0_1 Depth=1
	movl	(%rax), %eax
	decl	%eax
	movl	%eax, -8(%rbp)
	jmp	.LBB0_1
.LBB0_11:                               # %while_end10
	movb	-1(%rbp), %al
	movb	%al, -17(%rbp)
	movq	%rbp, %rsp
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end0:
	.size	isPerfectSquare, .Lfunc_end0-isPerfectSquare
	.cfi_endproc
                                        # -- End function
	.globl	main                            # -- Begin function main
	.p2align	4, 0x90
	.type	main,@function
main:                                   # @main
	.cfi_startproc
# %bb.0:
	subq	$24, %rsp
	.cfi_def_cfa_offset 32
	movq	%rdi, 16(%rsp)
	movl	value1(%rip), %edi
	callq	isPerfectSquare@PLT
	movzbl	%al, %edi
	andb	$1, %al
	movb	%al, 15(%rsp)
	callq	print_boolean@PLT
	addq	$24, %rsp
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end1:
	.size	main, .Lfunc_end1-main
	.cfi_endproc
                                        # -- End function
	.type	value1,@object                  # @value1
	.data
	.globl	value1
	.p2align	2
value1:
	.long	16                              # 0x10
	.size	value1, 4

	.section	".note.GNU-stack","",@progbits
