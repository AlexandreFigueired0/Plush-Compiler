# function print_int(val x : int); # FFI

function main() {
	var x : int := -1;
    while x < 5 {
        print_int(x);
        x := x + 1;
    }

    print_int(x);
    print_int(mult(x,2));
}

function mult(val x : int, val y : int) : int {
    mult := x *  y;
}

# function a(){
#     val x: [int] := get_int_array(5);
# }

