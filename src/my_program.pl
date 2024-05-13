# function print_int(val x : int); # FFI

function main() {
	# var x : int := -1;
    # while x < 5 {
    #     print_int(x);
    #     x := x + 1;
    # }

    # print_int(x);
    # print_int(mult(x,2));

    var x : [int] := get_int_array(5);
    x[0] := 10;
    var i : int := x[0];
    print_int(i);
}

function mult(val x : int, val y : int) : int {
    mult := x *  y;
}

function a() : [int]{
    val x: [int] := get_int_array(5);
    a := x;
}

