# function print_int(val x : int); # FFI

function main() {
    hello();
	var x : int := -1;
    while x < 5 {
        print_int(x);
        x := x + 1;
    }

    print_int(x);
    print_int(x^2);
}

function hello(){
    print_int(1);
}

