from compiler import run

def test_plush_array_binary_search():
    fname = "tests/arrayBinarySearch.pl"
    output = run(fname)
    assert output == "true"