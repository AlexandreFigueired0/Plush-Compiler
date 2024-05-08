# function print_int(val x : int); # FFI

function main() {
	var x : int := 1+1;
    if (x > 2) {
        x := 1;
    }

    print_int(x);
}