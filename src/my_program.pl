function foo (var x :int, val y :int): int {
    foo := x+y;
}

function main() {
    var a :int;
    var b :int;
    a := 1;
    b := 2;
    var c :int := foo("ola", b);
}