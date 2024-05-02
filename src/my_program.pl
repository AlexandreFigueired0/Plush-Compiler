# function get_array(): [[int]];
function print(val s : string);
function print_int(val x : int);

function double(val n : int) : int{
    double := n * 2;
}

function main(var args :int) {
    var x : int := 1 - 3 * 5;
    print_int(double(x));
}