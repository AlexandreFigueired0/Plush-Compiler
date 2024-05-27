function main(){
    val x : string := "test";
    val x_a : [char] := get_char_array(3);
    x_a[0] := '1';
    print_char(x_a[0]);
}