# Converts Binary to Decimal
# to test bit operations
			.data
array:		.space 128 # array[32]	
newLine:	.asciiz "\n\n"
newLine1:	.asciiz "\n"
space:		.asciiz " = "	
numbers:	.word 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 ,11, 12, 13, 14, 15, 16, 17, 18, 19, 20		
			
			.text
			.globl main
main:		li $t0, -4
			li $t1, -2147483648
			li $t2,  2147483648
			li $t3,  65
			move $a0, $t0
			jal print
			move $a0, $t1
			jal print
			move $a0, $t2
			jal print
			move $a0, $t3
			jal print
			la $a0, newLine1
			li $v0, 4
			syscall
			la $s1, numbers
			
			lw $a0, 0($s1)
			li $v0, 1
			syscall
			addi $s1, $s1, 4
			la $a0, newLine1
			li $v0, 4
			syscall
			srl $t4, $t0, 2		#1
			move $a0, $t4
			jal print
			
			lw $a0, 0($s1)
			li $v0, 1
			syscall
			addi $s1, $s1, 4
			la $a0, newLine1
			li $v0, 4
			syscall
			sra $t4, $t0, 2		#2
			move $a0, $t4
			jal print
			
			lw $a0, 0($s1)
			li $v0, 1
			syscall
			addi $s1, $s1, 4
			la $a0, newLine1
			li $v0, 4
			syscall
			sll $t4, $t0, 1		#3
			move $a0, $t4
			jal print
			
			lw $a0, 0($s1)
			li $v0, 1
			syscall
			addi $s1, $s1, 4
			la $a0, newLine1
			li $v0, 4
			syscall
			rol $t4, $t0, 2		#4
			move $a0, $t4
			jal print
			
			lw $a0, 0($s1)
			li $v0, 1
			syscall
			addi $s1, $s1, 4
			la $a0, newLine1
			li $v0, 4
			syscall
			ror $t4, $t0, 2		#5
			move $a0, $t4
			jal print
			
			lw $a0, 0($s1)
			li $v0, 1
			syscall
			addi $s1, $s1, 4
			la $a0, newLine1
			li $v0, 4
			syscall
			xor $t4, $t0, $t1	#6
			move $a0, $t4
			jal print
			
			lw $a0, 0($s1)
			li $v0, 1
			syscall
			addi $s1, $s1, 4
			la $a0, newLine1
			li $v0, 4
			syscall
			xor $t4, $t1, -8	#7
			move $a0, $t4
			jal print
			
			lw $a0, 0($s1)
			li $v0, 1
			syscall
			addi $s1, $s1, 4
			la $a0, newLine
			li $v0, 4
			syscall
			#add $t4, $t0, $t1	#8
			#move $a0, $t4
			#jal print
			
			lw $a0, 0($s1)
			li $v0, 1
			syscall
			addi $s1, $s1, 4
			la $a0, newLine1
			li $v0, 4
			syscall
			addu $t4, $t0, $t1	#9
			move $a0, $t4
			jal print
			
			lw $a0, 0($s1)
			li $v0, 1
			syscall
			addi $s1, $s1, 4
			la $a0, newLine1
			li $v0, 4
			syscall
			mul $t4, $t1, $t2	#10
			move $a0, $t4
			jal print
			
			lw $a0, 0($s1)
			li $v0, 1
			syscall
			addi $s1, $s1, 4
			la $a0, newLine
			li $v0, 4
			syscall
			#mulo $t4, $t1, $t2	#11
			#move $a0, $t4
			#jal print
			
			lw $a0, 0($s1)
			li $v0, 1
			syscall
			addi $s1, $s1, 4
			la $a0, newLine
			li $v0, 4
			syscall
			#mulou $t4, $t0, $t0	#12
			#move $a0, $t4
			#jal print
			
			lw $a0, 0($s1)
			li $v0, 1
			syscall
			addi $s1, $s1, 4
			la $a0, newLine1
			li $v0, 4
			syscall
			mulou $t4, $t3, $t3	#13
			move $a0, $t4
			jal print
			
			lw $a0, 0($s1)
			li $v0, 1
			syscall
			addi $s1, $s1, 4
			la $a0, newLine1
			li $v0, 4
			syscall
			div $t4, $t1, $t0	#14
			move $a0, $t4
			jal print
			
			lw $a0, 0($s1)
			li $v0, 1
			syscall
			addi $s1, $s1, 4
			la $a0, newLine1
			li $v0, 4
			syscall
			div $t4, $t3, $t0	#15
			move $a0, $t4
			jal print
			
			lw $a0, 0($s1)
			li $v0, 1
			syscall
			addi $s1, $s1, 4
			la $a0, newLine1
			li $v0, 4
			syscall
			divu $t4, $t1, $t0	#16
			move $a0, $t4
			jal print
			
			lw $a0, 0($s1)
			li $v0, 1
			syscall
			addi $s1, $s1, 4
			la $a0, newLine1
			li $v0, 4
			syscall
			sub $t4, $t1, $t0	#17
			move $a0, $t4
			jal print
			
			lw $a0, 0($s1)
			li $v0, 1
			syscall
			addi $s1, $s1, 4
			la $a0, newLine1
			li $v0, 4
			syscall
			subu $t4, $t1, $t0	#18
			move $a0, $t4
			jal print
			
			lw $a0, 0($s1)
			li $v0, 1
			syscall
			addi $s1, $s1, 4
			la $a0, newLine1
			li $v0, 4
			syscall
			mult $t1, $t2		#19
			mflo $s2		# save lo register before printing hi register 
			mfhi $a0
			jal print
			move $a0, $s2	# print lo register 
			jal print
			
			lw $a0, 0($s1)
			li $v0, 1
			syscall
			addi $s1, $s1, 4
			la $a0, newLine1
			li $v0, 4
			syscall
			multu $t0, $t3		#20
			mflo $s2
			mfhi $a0
			jal print
			move $a0, $s2
			jal print
			
			
			li $v0, 10
			syscall
	
# function that prints decimal value
# and converts decimal to binary, then prints binary value	
print:		move $t5, $a0		# save decimal value
			
			la $t9, array		# load binary array at 2^0 position
			addi $t9, $t9, 124
			li $t7, 32
			
			bgez $a0, loop	# if( $a0 > 0 ){ dont convert to two's compliment decimal}
			li $s0, 2147483647	# 2^31 - 1 (highest integer value possible)
			add $a0, $s0, $a0	# only syntax that works to convert
			addi $a0, $a0, 1	# because real formula uses 2^31
			
loop:		beqz $a0, bEQz		# if ($a0 == 0) {exit & push 0}
			rem $t8, $a0, 2		# $t8 = $a0 % 2
			sw $t8, 0($t9)		# push remainder
			div $a0, $a0, 2		# $a0 = $a0 / 2
			addi $t9, $t9, -4
			addi $t7, $t7, -1
			bgtz $a0, loop		# while( $a0 > 0){continue looping}

bEQz:		sw $zero, 0($t9)	# kinda like "base case"
			addi $t9, $t9, -4
			addi $t7, $t7, -1
			
fill0:		bltz $t7, fill1		# if ( reached 2^31 ){ stop filling }
			sw $zero, 0($t9)	# else{ fill array with zeros }
			addi $t9, $t9, -4
			addi $t7, $t7, -1
			j fill0
						
fill1:		bgez $t5, printB	# if( $a0 >= 0 ){ dont change sign}
			la $t9, array		# else{ change 'sign' of array }
			li $a1, 1 
			sw $a1, 0($t9)
			j printB		
			
printB:		la $t9, array		# print binary number
			li $t7, 32
bLoop:		lw $a0, 0($t9)
			li $v0, 1
			syscall
			addi $t9, $t9, 4
			addi $t7, $t7, -1
			bgtz $t7, bLoop
			
			la $a0, space		# print decimal value
			li $v0, 4
			syscall
			move $a0, $t5
			li $v0, 1			
			syscall
			
			la $a0, newLine		# finally done
			li $v0, 4
			syscall
			jr $ra