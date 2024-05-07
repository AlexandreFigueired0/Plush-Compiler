function print_int(val x : int); # FFI

function main() {
	val x : int := 1+1;
    if (x > 1) {
        print_int(x);
    }
}