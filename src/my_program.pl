function get_array(): [int];

function foo (var x :[int]): int;

function foo (var y :[int]): int {

    foo:=1;
}

function main(var args :int) {
    var a :[int] := get_array();
    var c :int := a[foo(a)];
    args :=1;
    c :=1;
}