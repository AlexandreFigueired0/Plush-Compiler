function print_bool(val b:boolean);
function print_int(val i:int);

val value : int := 16;

#implemented using binary search
function isPerfectSquare(val n:int) : boolean {
    var result : boolean := false;
    var low : int := 1;
    var high : int := n;

    while low <= high && !result {
        var mid : int := low + ((high - low) / 2); # safe average
        var square : int := mid * mid;
        if square = n {
            result := true;
        } 
        if square != n && square < n {
            low := mid + 1;
        } 
        if square != n && !(square < n) {
            high := mid - 1;
        }
    }

    isPerfectSquare := result;
}

function main(val args:[string]) {
	val result : boolean := isPerfectSquare(value);
	print_bool(result); # should print true
}
