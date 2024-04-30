function get_array(): [int];

function foo (var x :[int]): int {

    foo:=1;
}

function main() {
    var a :[int] := get_array();
    var c :int := a[foo(a)];
}