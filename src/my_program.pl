# function print_int(val x : int); # FFI

function main() {

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

