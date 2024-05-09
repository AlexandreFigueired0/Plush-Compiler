# function print_int(val x : int); # FFI

function main() {
	var x : int := -1;
    while x < 5 {
        print_int(x);
        x := x + 1;
    }

    print_int(x);
}