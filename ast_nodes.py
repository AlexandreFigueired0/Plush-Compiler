from dataclasses import dataclass
from abc import ABC

# All fields have default value, because it will be easier to create instances of these classes
# without having to provide all the fields.
# This comes with the cost of having more trouble to debug, because there will be no error if a field is not provided.

@dataclass
class Node(ABC):
    line_start: int = 0
    column_start: int = 0
    line_end: int = 0
    column_end: int = 0
    

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


# DECLARATIONS

@dataclass
class ValParam(Node):
    name: str = None
    type_: Type = None

    def __str__(self):
        return f"val {self.name} : {self.type_}"

@dataclass
class VarParam(Node):
    name: str = None
    type_: Type = None

    def __str__(self):
        return f"var {self.name} : {self.type_}"


@dataclass
class FunctionDeclaration(Node):
    name: str = None
    params: list = None
    type_: Type = None

    def __str__(self):
        return f"function {self.name} ({', '.join(map(str, self.params))}) : {self.type_}"


# DEFINITIONS

@dataclass
class ValDefinition(Node):
    name: str = None
    type_: Type = None
    expr: Expression = None

    def __str__(self):
        return f"val {self.name} : {self.type_} := {self.expr}"


@dataclass
class VarDefinition(Node):
    name: str = None
    type_: Type = None
    expr: Expression = None

    def __str__(self):
        return f"var {self.name} : {self.type_} := {self.expr}"


@dataclass
class FunctionDefinition(Node):
    name: str = None
    params: list = None
    type_: Type = None
    block: list = None

    def __str__(self):
        return f"function {self.name} ({', '.join(map(str, self.params))}) : {self.type_} {self.block}"


@dataclass
class Assignment(Node):
    name: str = None
    expr: Expression = None

    def __str__(self):
        return f"{self.name} := {self.expr}"

@dataclass
class ArrayPositionAssignment(Node):
    name: str = None
    indexes: list[Expression] = None
    expr: Expression = None

    def __str__(self):
        return f"{self.name} [{', '.join(map(str, self.indexes))}] := {self.expr}"


# STATEMENTS

@dataclass
class If(Node):
    condition: Expression = None
    block: list = None

    def __str__(self):
        return f"if {self.condition} {self.block}"


@dataclass
class IfElse(Node):
    condition: Expression = None
    block: list = None
    else_block: list = None

    def __str__(self):
        return f"if {self.condition} {self.block} else {self.else_block}"

@dataclass
class While(Node):
    condition: Expression = None
    block: list = None

    def __str__(self):
        return f"while {self.condition} {self.block}"



# TYPES

@dataclass
class IntType(Type):
    def __str__(self):
        return "int"
    def __eq__(self, other):
        return isinstance(other, IntType)

@dataclass
class FloatType(Type):
    def __str__(self):
        return "float"
    def __eq__(self, other):
        return isinstance(other, FloatType)

@dataclass
class BooleanType(Type):
    def __str__(self):
        return "boolean"
    def __eq__(self, other):
        return isinstance(other, BooleanType)

@dataclass
class StringType(Type):
    def __str__(self):
        return "string"
    def __eq__(self, other):
        return isinstance(other, StringType)

@dataclass
class CharType(Type):
    def __str__(self):
        return "char"
    def __eq__(self, other):
        return isinstance(other, CharType)


@dataclass
class ArrayType(Type):
    type_: Type = None

    def __str__(self):
        return f"array of {self.type_}"
    
    def __eq__(self, other):
        if isinstance(other, ArrayType):
            return self.type_ == other.type_
        return False


# EXPRESSIONS

@dataclass
class FunctionCall(Expression):
    name: str = None
    args: list = None

    def __str__(self):
        return f"{self.name} ({', '.join(map(str, self.args))})"

@dataclass
class Or(Expression):
    left: Expression = None
    right: Expression = None

    def __str__(self):
        return f"{self.left} || {self.right}"


@dataclass
class And(Expression):
    left: Expression = None
    right: Expression = None

    def __str__(self):
        return f"{self.left} && {self.right}"

@dataclass
class Equal(Expression):
    left: Expression = None
    right: Expression = None

    def __str__(self):
        return f"{self.left} = {self.right}"

@dataclass
class NotEqual(Expression):
    left: Expression = None
    right: Expression = None

    def __str__(self):
        return f"{self.left} != {self.right}"

@dataclass
class LessThan(Expression):
    left: Expression = None
    right: Expression  = None

    def __str__(self):
        return f"{self.left} < {self.right}"
@dataclass
class GreaterThan(Expression):
    left: Expression = None
    right: Expression = None

    def __str__(self):
        return f"{self.left} > {self.right}"

@dataclass
class LessThanOrEqual(Expression):
    left: Expression = None
    right: Expression = None

    def __str__(self):
        return f"{self.left} <= {self.right}"

@dataclass
class GreaterThanOrEqual(Expression):
    left: Expression = None
    right: Expression = None

    def __str__(self):
        return f"{self.left} >= {self.right}"

@dataclass
class Add(Expression):
    left: Expression = None
    right: Expression = None

    def __str__(self):
        return f"{self.left} + {self.right}"


@dataclass
class Sub(Expression):
    left: Expression = None
    right: Expression = None

    def __str__(self):
        return f"{self.left} - {self.right}"


@dataclass
class Power(Expression):
    left: Expression = None
    right: Expression = None

    def __str__(self):
        return f"{self.left} ^ {self.right}"


@dataclass
class Mul(Expression):
    left: Expression = None
    right: Expression = None

    def __str__(self):
        return f"{self.left} * {self.right}"


@dataclass
class Div(Expression):
    left: Expression= None
    right: Expression = None

    def __str__(self):
        return f"{self.left} / {self.right}"

@dataclass
class Mod(Expression):
    left: Expression= None
    right: Expression = None

    def __str__(self):
        return f"{self.left} % {self.right}"

@dataclass
class UnaryMinus(Expression):
    expr: Expression = None

    def __str__(self):
        return f"-{self.expr}"


@dataclass
class LogicNot(Expression):
    expr: Expression = None

    def __str__(self):
        return f"!{self.expr}"


@dataclass
class ArrayAccess(Expression):
    name: str = None
    indexes: list[Expression] = None

    def __str__(self):
        return f"{self.name} [{', '.join(map(str, self.indexes))}]"

@dataclass
class FunctionCallArrayAccess(Expression):
    fcall: FunctionCall = None
    indexes: list[Expression] = None

    def __str__(self):
        return f"{self.fcall} [{', '.join(map(str, self.indexes))}]"

@dataclass
class Id(Expression):
    name: str = None

    def __str__(self):
        return self.name


@dataclass
class IntLit(Expression):
    value: int= None

    def __str__(self):
        return str(self.value)

    

@dataclass
class FloatLit(Expression):
    value: float = None

    def __str__(self):
        return str(self.value)

@dataclass
class CharLit(Expression):
    value: str = None

    def __str__(self):
        return f"\'{str(self.value)}\'"

@dataclass
class BooleanLit(Expression):
    value: bool = None

    def __str__(self):
        return str(self.value)


@dataclass
class String(Expression):
    value: str = None

    def __str__(self):
        return f"""\"{str(self.value)}\""""

