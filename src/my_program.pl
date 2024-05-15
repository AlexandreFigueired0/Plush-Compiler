val array_size : int := 10;

function binary_search(val arr : [int], val x : int) : boolean {
    var left : int := 0;
    var right : int := array_size- 1;
    var ret_val : boolean := false;
    while !ret_val && left <= right{
        var mid : int := left + (right - left) / 2;
        if arr[mid] = x {
            ret_val := true;
        }
        if arr[mid] < x {
            left := mid + 1;
        } else {
            right := mid - 1;
        }
    }
    binary_search := ret_val;
}

function main() {
    val my_array : [int] := get_int_array(array_size);
    var i : int := 0;
    while i < array_size {
        my_array[i] := i;
        i := i + 1;
    }
    print_boolean(binary_search(my_array, 9));
    
}


