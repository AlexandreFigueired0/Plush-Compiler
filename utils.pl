from utils2 import hello_world

function print_matrix(val m : [[int]], val rows : int, val cols : int){
    var i : int := 0;
    while i < rows{
        print_int_array(m[i], cols);
        i := i + 1;
    }
}

function hello(){
    hello_world();
}