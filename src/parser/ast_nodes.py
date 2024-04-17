from dataclasses import dataclass
from abc import ABC

@dataclass
class Type(ABC):
    pass

@dataclass
class Expression(ABC):
    pass


# DECLARATIONS

@dataclass
class ValDeclaration:
    name: str
    type_: Type

@dataclass
class VarDeclaration:
    name: str
    type_: Type

@dataclass
class ValParam:
    name: str
    type_: Type

@dataclass
class VarParam:
    name: str
    type_: Type

@dataclass
class FunctionDeclaration:
    name: str
    params: list
    type_: Type

# DEFINITIONS

@dataclass
class ValDefinition:
    name: str
    type_: Type
    expr: Expression

@dataclass
class VarDefinition:
    name: str
    type_: Type
    expr: Expression

@dataclass
class FunctionDefinition:
    name: str
    params: list
    type_: Type
    block: list

@dataclass
class Assignment:
    name: str
    expr: Expression

@dataclass
class ArrayPositionAssignment:
    name: str
    position: Expression
    expr: Expression

# STATEMENTS

@dataclass
class If():
    condition: Expression
    block: list

@dataclass
class IfElse():
    condition: Expression
    block: list
    else_block: list

@dataclass
class While():
    condition: Expression
    block: list

@dataclass
class FunctionCall():
    name: str
    args: list

# EXPRESSIONS

@dataclass
class Id(Expression):
    name: str

@dataclass
class IntLit(Expression):
    value: int

@dataclass
class FloatLit(Expression):
    value: float

@dataclass
class BooleanLit(Expression):
    value: bool

@dataclass
class String(Expression):
    value: str

# TYPES

@dataclass
class IntType(Type):
    pass

@dataclass
class FloatType(Type):
    pass

@dataclass
class DoubleType(Type):
    pass

@dataclass
class StringType(Type):
    pass

@dataclass
class BooleanType(Type):
    pass

@dataclass
class ArrayType(Type):
    type_: Type
