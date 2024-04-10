from my_parser import parse_plush

program = """
        val x: int;
    """
# Example usage
program_ast = parse_plush(program)

print(program_ast)



