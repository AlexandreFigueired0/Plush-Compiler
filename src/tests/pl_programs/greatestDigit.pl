# function print_int(val n:int);

val value : int := 1290;

function greatestDigit(var n:int) : int {
    var max : int := 0;
    while n > 1 {
        var digit : int := n % 10;
        if digit > max {
            max := digit;
        }
        n := n / 10;
    }
    greatestDigit := max;
}

function main(val args:[string]) {
	val result : int := greatestDigit(value);
	print_int(result); # prints 9
}