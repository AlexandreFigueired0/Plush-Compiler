# function print_int(val x : int); # FFI

function main() {
    val a : [int] := get_int_array(12);
    a[4] := -2;
    print_int(a[4]);
}


