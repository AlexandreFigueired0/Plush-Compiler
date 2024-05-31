	.text
	.file	"code.ll"
	.globl	binary_search                   # -- Begin function binary_search
	.p2align	4, 0x90
	.type	binary_search,@function
binary_search:                          # @binary_search
	.cfi_startproc
# %bb.0:
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	subq	$32, %rsp
	movq	%rdi, -32(%rbp)
	movl	%esi, -20(%rbp)
	movl	$0, -12(%rbp)
	movl	array_size1(%rip), %eax
	decl	%eax
	movl	%eax, -8(%rbp)
	movb	$0, -1(%rbp)
	cmpb	$1, -1(%rbp)
	jne	.LBB0_2
	jmp	.LBB0_8
	.p2align	4, 0x90
.LBB0_7:                                # %else41
                                        #   in Loop: Header=BB0_2 Depth=1
	movl	(%rax), %eax
	decl	%eax
	movl	%eax, -8(%rbp)
	cmpb	$1, -1(%rbp)
	je	.LBB0_8
.LBB0_2:                                # %while_cond10
                                        # =>This Inner Loop Header: Depth=1
	movl	-8(%rbp), %eax
	cmpl	%eax, -12(%rbp)
	jg	.LBB0_8
# %bb.3:                                # %while_body11
                                        #   in Loop: Header=BB0_2 Depth=1
	movq	%rsp, %rcx
	leaq	-16(%rcx), %rax
	movq	%rax, %rsp
	movl	-12(%rbp), %edx
	movl	-8(%rbp), %esi
	subl	%edx, %esi
	movl	%esi, %edi
	shrl	$31, %edi
	addl	%esi, %edi
	sarl	%edi
	addl	%edx, %edi
	movl	%edi, -16(%rcx)
	movq	-32(%rbp), %rcx
	movslq	%edi, %rdx
	movl	(%rcx,%rdx,4), %ecx
	cmpl	-20(%rbp), %ecx
	jne	.LBB0_5
# %bb.4:                                # %if_true32
                                        #   in Loop: Header=BB0_2 Depth=1
	movb	$1, -1(%rbp)
.LBB0_5:                                # %if_end33
                                        #   in Loop: Header=BB0_2 Depth=1
	movq	-32(%rbp), %rcx
	movslq	(%rax), %rdx
	movl	(%rcx,%rdx,4), %ecx
	cmpl	-20(%rbp), %ecx
	jge	.LBB0_7
# %bb.6:                                # %if_true40
                                        #   in Loop: Header=BB0_2 Depth=1
	movl	(%rax), %eax
	incl	%eax
	movl	%eax, -12(%rbp)
	cmpb	$1, -1(%rbp)
	jne	.LBB0_2
.LBB0_8:                                # %while_end12
	movb	-1(%rbp), %al
	movb	%al, -13(%rbp)
	movq	%rbp, %rsp
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end0:
	.size	binary_search, .Lfunc_end0-binary_search
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
	movl	array_size1(%rip), %edi
	callq	get_int_array@PLT
	movq	%rax, 16(%rsp)
	movl	$0, 12(%rsp)
	.p2align	4, 0x90
.LBB1_1:                                # %while_cond53
                                        # =>This Inner Loop Header: Depth=1
	movl	12(%rsp), %eax
	cmpl	array_size1(%rip), %eax
	jge	.LBB1_3
# %bb.2:                                # %while_body54
                                        #   in Loop: Header=BB1_1 Depth=1
	movq	16(%rsp), %rax
	movslq	12(%rsp), %rcx
	movl	%ecx, (%rax,%rcx,4)
	incl	12(%rsp)
	jmp	.LBB1_1
.LBB1_3:                                # %while_end55
	movq	16(%rsp), %rdi
	movl	$91, %esi
	callq	binary_search@PLT
	movzbl	%al, %edi
	callq	print_boolean@PLT
	addq	$24, %rsp
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end1:
	.size	main, .Lfunc_end1-main
	.cfi_endproc
                                        # -- End function
	.type	array_size1,@object             # @array_size1
	.data
	.globl	array_size1
	.p2align	2
array_size1:
	.long	10                              # 0xa
	.size	array_size1, 4

	.section	".note.GNU-stack","",@progbits
