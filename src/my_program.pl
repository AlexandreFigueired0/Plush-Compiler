# function print_int(val x : int); # FFI

function main() {
	var x : int := 10 * 1;
    if x > 0 {
        x := 1;
    }
    else{
        x := 2;
    }

    print_int(x);
}