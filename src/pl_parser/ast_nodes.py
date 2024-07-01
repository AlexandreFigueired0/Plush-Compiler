from dataclasses import dataclass, asdict
from abc import ABC

# All fields have default value, because it will be easier to create instances of these classes
# without having to provide all the fields.
# This comes with the cost of having more trouble to debug, because there will be no error if a field is not provided.

@dataclass
class Node(ABC):
    line: int = 0
    column: int = 0
    end_line: int = 0
    end_column: int = 0
    text : str = ""
    

@dataclass
class Type(Node):
    pass

@dataclass
class Expression(Node):
    type_: Type = None
# START

@dataclass
class Start():
    defs_or_decls: list = None

# IMPORT

@dataclass
class Import:
    file : str
    func_names : list

# DECLARATIONS

@dataclass
class ValParam(Node):
    name: str = None
    type_: Type = None


@dataclass
class VarParam(Node):
    name: str = None
    type_: Type = None




@dataclass
class FunctionDeclaration(Node):
    name: str = None
    params: list = None
    type_: Type = None




# DEFINITIONS

@dataclass
class ValDefinition(Node):
    name: str = None
    type_: Type = None
    expr: Expression = None



@dataclass
class VarDefinition(Node):
    name: str = None
    type_: Type = None
    expr: Expression = None



@dataclass
class FunctionDefinition(Node):
    name: str = None
    params: list = None
    type_: Type = None
    block: list = None




@dataclass
class Assignment(Node):
    name: str = None
    expr: Expression = None



@dataclass
class ArrayPositionAssignment(Node):
    name: str = None
    indexes: list[Expression] = None
    expr: Expression = None



# STATEMENTS

@dataclass
class If(Node):
    condition: Expression = None
    block: list = None



@dataclass
class IfElse(Node):
    condition: Expression = None
    block: list = None
    else_block: list = None


@dataclass
class While(Node):
    condition: Expression = None
    block: list = None





# TYPES

@dataclass
class IntType(Type):
    text : str= "int"
    def __eq__(self, other):
        return isinstance(other, IntType)

@dataclass
class FloatType(Type):
    text : str= "float"
    def __eq__(self, other):
        return isinstance(other, FloatType)

@dataclass
class BooleanType(Type):
    text : str = "boolean"
    def __eq__(self, other):
        return isinstance(other, BooleanType)

@dataclass
class StringType(Type):
    text : str = "string"
    def __eq__(self, other):
        return isinstance(other, StringType)

@dataclass
class CharType(Type):
    text : str = "char"
    def __eq__(self, other):
        return isinstance(other, CharType)


@dataclass
class ArrayType(Type):
    type_: Type = None


    text : str= f"[{type_.text}]" if type_ else "[]"
    
    def __eq__(self, other):
        if isinstance(other, ArrayType):
            return self.type_ == other.type_
        return False


# EXPRESSIONS

@dataclass
class FunctionCall(Expression):
    name: str = None
    args: list = None



@dataclass
class Or(Expression):
    left: Expression = None
    right: Expression = None



@dataclass
class And(Expression):
    left: Expression = None
    right: Expression = None


@dataclass
class Equal(Expression):
    left: Expression = None
    right: Expression = None



@dataclass
class NotEqual(Expression):
    left: Expression = None
    right: Expression = None



@dataclass
class LessThan(Expression):
    left: Expression = None
    right: Expression  = None


@dataclass
class GreaterThan(Expression):
    left: Expression = None
    right: Expression = None



@dataclass
class LessThanOrEqual(Expression):
    left: Expression = None
    right: Expression = None



@dataclass
class GreaterThanOrEqual(Expression):
    left: Expression = None
    right: Expression = None



@dataclass
class Add(Expression):
    left: Expression = None
    right: Expression = None




@dataclass
class Sub(Expression):
    left: Expression = None
    right: Expression = None




@dataclass
class Power(Expression):
    left: Expression = None
    right: Expression = None




@dataclass
class Mul(Expression):
    left: Expression = None
    right: Expression = None



@dataclass
class Div(Expression):
    left: Expression= None
    right: Expression = None


@dataclass
class Mod(Expression):
    left: Expression= None
    right: Expression = None


@dataclass
class UnaryMinus(Expression):
    expr: Expression = None




@dataclass
class LogicNot(Expression):
    expr: Expression = None



@dataclass
class ArrayAccess(Expression):
    name: str = None
    indexes: list[Expression] = None


@dataclass
class FunctionCallArrayAccess(Expression):
    fcall: FunctionCall = None
    indexes: list[Expression] = None



@dataclass
class Id(Expression):
    name: str = None

@dataclass
class IntLit(Expression):
    value: int= None

    

@dataclass
class FloatLit(Expression):
    value: float = None

@dataclass
class CharLit(Expression):
    value: str = None


@dataclass
class BooleanLit(Expression):
    value: bool = None


@dataclass
class String(Expression):
    value: str = None

import json

def node_to_json(node):
    return json.dumps(asdict(node), default=str,  indent=4)