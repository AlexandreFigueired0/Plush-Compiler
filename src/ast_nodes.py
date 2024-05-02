from dataclasses import dataclass
from abc import ABC

@dataclass
class Type(ABC):
    pass

@dataclass
class Expression(ABC):
    pass
# START

@dataclass
class Start:
    defs_or_decls: list


# DECLARATIONS

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
    indexes: list[Expression]
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



# EXPRESSIONS

@dataclass
class FunctionCall():
    name: str
    args: list
    type_: Type = None

@dataclass
class Or(Expression):
    left: Expression
    right: Expression


@dataclass
class And(Expression):
    left: Expression
    right: Expression


@dataclass
class Equal(Expression):
    left: Expression
    right: Expression


@dataclass
class NotEqual(Expression):
    left: Expression
    right: Expression


@dataclass
class LessThan(Expression):
    left: Expression
    right: Expression

@dataclass
class GreaterThan(Expression):
    left: Expression
    right: Expression


@dataclass
class LessThanOrEqual(Expression):
    left: Expression
    right: Expression


@dataclass
class GreaterThanOrEqual(Expression):
    left: Expression
    right: Expression


@dataclass
class Add(Expression):
    left: Expression
    right: Expression
    type_: Type = None


@dataclass
class Sub(Expression):
    left: Expression
    right: Expression
    type_: Type = None


@dataclass
class Power(Expression):
    left: Expression
    right: Expression
    type_: Type = None


@dataclass
class Mul(Expression):
    left: Expression
    right: Expression
    type_: Type = None


@dataclass
class Div(Expression):
    left: Expression
    right: Expression
    type_: Type = None

@dataclass
class Mod(Expression):
    left: Expression
    right: Expression
    type_: Type = None

@dataclass
class UnaryMinus(Expression):
    expr: Expression
    type_: Type = None


@dataclass
class LogicNot(Expression):
    expr: Expression


@dataclass
class ArrayAccess(Expression):
    name: str
    indexes: list[Expression]
    type_: Type = None

@dataclass
class Id(Expression):
    name: str
    type_: Type = None


@dataclass
class IntLit(Expression):
    value: int

    

@dataclass
class FloatLit(Expression):
    value: float

@dataclass
class CharLit(Expression):
    value: str

@dataclass
class BooleanLit(Expression):
    value: bool


@dataclass
class String(Expression):
    value: str


# TYPES

@dataclass
class IntType(Type):
    def __str__(self):
        return "int"

@dataclass
class FloatType(Type):
    def __str__(self):
        return "float"

@dataclass
class DoubleType(Type):
    def __str__(self):
        return "double"

@dataclass
class StringType(Type):
    def __str__(self):
        return "string"

@dataclass
class CharType(Type):
    def __str__(self):
        return "char"

@dataclass
class BooleanType(Type):
    def __str__(self):
        return "boolean"

@dataclass
class ArrayType(Type):
    type_: Type

    def __str__(self):
        return f"array of {self.type_}"
