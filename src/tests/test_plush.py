from src.compiler.compiler import run

def test_plush_array_binary_search():
    fname = "tests/pl_programs/arrayBinarySearch.pl"
    output = run(fname)
    assert output == "true\n"

def test_plush_greatest_digit():
    fname = "tests/pl_programs/greatestDigit.pl"
    output = run(fname)
    assert output == "9\n"

def test_plush_is_palindrome_number():
    fname = "tests/pl_programs/isPalindromeNumber.pl"
    output = run(fname)
    assert output == "true\n"

def test_plush_is_perfect_square():
    fname = "tests/pl_programs/isPerfectSquare.pl"
    output = run(fname)
    assert output == "true\n"

def test_plush_matrix_product():
    fname = "tests/pl_programs/matrixProduct.pl"
    output = run(fname)
    expected =\
"""\
7 10 
15 22 
23 34 
"""
    assert output == expected