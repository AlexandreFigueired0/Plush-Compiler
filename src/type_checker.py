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
            ctx.set_type(name, type_)
        case "assignment":
            name, expr = node.children
            #TODO: Check if variable is already declared
            if not ctx.has_var(name):
                raise TypeError(f"Variable {name} doesn't exist")
            
            var_type = ctx.get_type(name)
            expr_type = type_check(ctx, expr)
            if var_type != expr_type:
                raise TypeError(f"Type mismatch for variable {name}, expected {var_type} but got {expr_type}")
            

        # TODO: como e que é para estas ops entre ints e floats?
        # TODO: comparaçao de grandeza entre strings?
        case "add" | "sub" | "mul" | "div" | "power" | "lt" | "gt" | "lte" | "gte":
            left_tree, right_tree = node.children
            left_type = type_check(ctx, left_tree)
            right_type = type_check(ctx, right_tree)

            #TODO: como aprsentar este erro
            if (left_type == "int" or left_type == "float") and (right_type == "int" or right_type == "float"):
                return "float" if "float" in [left_type, right_type] else "int"
            
            wrong_type = left_type if left_type != "int" and left_type != "float" else right_type
            raise TypeError(f"Type mismatch for {node.data}, expected ints or floats but found a {wrong_type}")
                
        case "id":
            name = node.children[0]
            return ctx.get_type(name)
        case "int_lit":
            return "int"
        case "boolean_lit":
            return "boolean"
        case "float_lit":
            return "float"
        case "string":
            return "string"
        case _:
            raise TypeError(f"Unknown node type {node.data}")
            
            

            
if __name__ == "__main__":
    program = """
        val y: boolean := true;
        x := 1;
    """
    # Example usage
    program_ast = parse_plush(program)
    print(program_ast.pretty())
    type_check(Context(), program_ast)