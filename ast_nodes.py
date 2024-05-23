from dataclasses import dataclass
from abc import ABC

@dataclass
class Node(ABC):
    line_start: int
    column_start: int
    line_end: int
    column_end: int

@dataclass
class Type(Node):
    pass

@dataclass
class Expression(Node):
    type_: Type
# START

@dataclass
class Start():
    defs_or_decls: list


# DECLARATIONS

@dataclass
class ValParam(Node):
    name: str
    type_: Type

@dataclass
class VarParam(Node):
    name: str
    type_: Type


@dataclass
class FunctionDeclaration(Node):
    name: str
    params: list
    type_: Type


# DEFINITIONS

@dataclass
class ValDefinition(Node):
    name: str
    type_: Type
    expr: Expression


@dataclass
class VarDefinition(Node):
    name: str
    type_: Type
    expr: Expression


@dataclass
class FunctionDefinition(Node):
    name: str
    params: list
    type_: Type
    block: list


@dataclass
class Assignment(Node):
    name: str
    expr: Expression

@dataclass
class ArrayPositionAssignment(Node):
    name: str
    indexes: list[Expression]
    expr: Expression


# STATEMENTS

@dataclass
class If(Node):
    condition: Expression
    block: list


@dataclass
class IfElse(Node):
    condition: Expression
    block: list
    else_block: list

@dataclass
class While(Node):
    condition: Expression
    block: list



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
class BooleanType(Type):
    def __str__(self):
        return "boolean"

@dataclass
class StringType(Type):
    def __str__(self):
        return "string"

@dataclass
class CharType(Type):
    def __str__(self):
        return "char"


@dataclass
class ArrayType(Type):
    type_: Type

    def __str__(self):
        return f"array of {self.type_}"


# EXPRESSIONS

@dataclass
class FunctionCall(Expression):
    name: str
    args: list

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


@dataclass
class Sub(Expression):
    left: Expression
    right: Expression


@dataclass
class Power(Expression):
    left: Expression
    right: Expression


@dataclass
class Mul(Expression):
    left: Expression
    right: Expression


@dataclass
class Div(Expression):
    left: Expression
    right: Expression

@dataclass
class Mod(Expression):
    left: Expression
    right: Expression

@dataclass
class UnaryMinus(Expression):
    expr: Expression


@dataclass
class LogicNot(Expression):
    expr: Expression


@dataclass
class ArrayAccess(Expression):
    name: str
    indexes: list[Expression]

@dataclass
class FunctionCallArrayAccess(Expression):
    fcall: FunctionCall
    indexes: list[Expression]

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
class CharLit(Expression):
    value: str

@dataclass
class BooleanLit(Expression):
    value: bool


@dataclass
class String(Expression):
    value: str

