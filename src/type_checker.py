from my_parser import parse_plush
from dataclasses import dataclass
from lark import Tree, Token

class Context():
    def __init__(self):
        self.stack = [{}]
    
    def get_type(self, name):
        for scope in self.stack[::-1]:
            if name in scope:
                return scope[name]
        raise TypeError(f"Variable {name} doesn't exist")
    
    def set_type(self, name, value):
        scope = self.stack[0]
        scope[name] = value

    def has_var(self, name):
        for scope in self.stack[::-1]:
            if name in scope:
                return True
        return False
    
    def has_var_in_current_scope(self, name):
        return name in self.stack[-1]
    
    def enter_block(self):
        self.stack.append({})
    
    def exit_block(self):
        self.stack.pop()

def type_check(ctx : Context, node: Tree) -> bool:
    match node.data:
        case "start":
            for child in node.children:
                type_check(ctx, child)
        case "val_declaration" | "var_declaration":
            name, type_tree = node.children
            type_ = type_tree.data.replace("_type", "")
            #TODO: Check if variable is already declared
            #TODO: Is this ok even if the prev ctx has this name
            if ctx.has_var_in_current_scope(name):
                raise TypeError(f"Variable {name} already declared")

            ctx.set_type(name, type_)
        case "val_definition" | "var_definition":
            name, type_tree, expr = node.children
            type_ = type_tree.data.replace("_type", "")

            if ctx.has_var_in_current_scope(name):
                raise TypeError(f"Variable {name} already declared")
            
            expr_type = type_check(ctx, expr)
            if type_ != expr_type:
                raise TypeError(f"Type mismatch for variable {name}, expected {type_} but got {expr_type}")
        case "add" | "sub" | "mul" | "div" | "power" | "lt" | "gt" | "lte" | "gte" | "equal" | "not_equal":
            left_tree, right_tree = node.children
            left_type = type_check(ctx, left_tree)
            right_type = type_check(ctx, right_tree)
            #TODO: como aprsentar este erro
            if (left_type ,right_type) == ("int", "int") or (left_type ,right_type) == ("float", "float"):
                return left_type
            
            raise TypeError(f"Type mismatch for addition, expected ints or floats but got {left_type} {right_type}")
                

        case "int_lit":
            return "int"
        case "boolean_lit":
            return "boolean"
        case _:
            raise TypeError(f"Unknown node type {node.data}")
            
            

            
if __name__ == "__main__":
    program = """
        val x: int := 1 + 1 - 1 * 1;
    """
    # Example usage
    program_ast = parse_plush(program)
    print(program_ast.pretty())
    result = type_check(Context(), program_ast)