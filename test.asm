# Testing ASM
li $t0, 5                               # Or from an immediate (constant)
li $t1, 6
add $t2, $t0, $t1                       # $t2 = $t0 + $t1
sub $t2, $t0, $t2                       # $t2 = $t0 - $t2
mul $t2, $t0, $t1                       # $t2 = $t0 * $t1
div $t2, $t0, $t1                       # $t2 = $t0 / $t1
xor $t3, $t2, $t1                       # $t3 = $t2 xor $t1