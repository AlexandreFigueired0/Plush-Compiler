# function print_boolean(val b: boolean);
# function print_int(val i: int);

val value : int := 12321;

function digits(val num:int) : int {
    var n : int := num;
    var count : int := 0;
    while n > 0 {
        count := count + 1;
        n := n / 10;
    }
    digits := count;
}

# Not the best implementation, but its a good one to understand the language
function isPalindromeNumber(var n:int) : boolean {
    var result : boolean := true;
    if n < 0 {
        result := false;
    } # not sure if this else is needed
    else {
        var n_digits : int := digits(n);

        while n_digits > 1 {
            var left : int := n / (10 ^ (n_digits - 1));
            var right : int := n % 10;
            if left != right {
                result := false;
            }
            n := n / 10; # remove right digit
            n := n % (10 ^ (n_digits - 2)); # remove left digit
            n_digits := n_digits - 2;
        }
        
        isPalindromeNumber := result;
    }
}



function main(val args:[string]) {
	val result : boolean := isPalindromeNumber(value);
	print_boolean(result); # prints true
}
