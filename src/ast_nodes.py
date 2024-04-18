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

    def __str__(self):
        res = ""
        for def_or_decl in self.defs_or_decls:
            res += str(def_or_decl) + "\n"
        return res
            
        

# DECLARATIONS

@dataclass
class ValDeclaration:
    name: str
    type_: Type

    def __str__(self):
        return f"val {self.name} : {self.type_};"

@dataclass
class VarDeclaration:
    name: str
    type_: Type

    def __str__(self):
        return f"var {self.name} : {self.type_};"

@dataclass
class ValParam:
    name: str
    type_: Type

    def __str__(self):
        return f"val {self.name} : {self.type_}"

@dataclass
class VarParam:
    name: str
    type_: Type

    def __str__(self):
        return f"var {self.name} : {self.type_}"

@dataclass
class FunctionDeclaration:
    name: str
    params: list
    type_: Type

    def __str__(self):
        return f"function {self.name}({', '.join(map(str, self.params))}) : {self.type_};"

# DEFINITIONS

@dataclass
class ValDefinition:
    name: str
    type_: Type
    expr: Expression

    def __str__(self):
        return f"val {self.name} : {self.type_} := {self.expr};"

@dataclass
class VarDefinition:
    name: str
    type_: Type
    expr: Expression

    def __str__(self):
        return f"var {self.name} : {self.type_} := {self.expr};"

@dataclass
class FunctionDefinition:
    name: str
    params: list
    type_: Type
    block: list

    def __str__(self):
        return f"function {self.name}({', '.join(map(str, self.params))}) : {self.type_} {{\n{'\n'.join(map(str, self.block))}\n}}"

@dataclass
class Assignment:
    name: str
    expr: Expression

    def __str__(self):
        return f"{self.name} := {self.expr};"

@dataclass
class ArrayPositionAssignment:
    name: str
    indexes: list[Expression]
    expr: Expression

    def __str__(self):
        return f"{self.name}{''.join(map(lambda i: f"[{i}]", self.indexes))} := {self.expr};"

# STATEMENTS

@dataclass
class If():
    condition: Expression
    block: list

    def __str__(self):
        return f"if {self.condition} {{\n{'\n'.join(map(str, self.block))}\n}}"

@dataclass
class IfElse():
    condition: Expression
    block: list
    else_block: list

    def __str__(self):
        return f"if {self.condition} {{\n{'\n'.join(map(str, self.block))}\n}} else {{\n{'\n'.join(map(str, self.else_block))}\n}}"

@dataclass
class While():
    condition: Expression
    block: list

    def __str__(self):
        return f"while {self.condition} {{\n{'\n'.join(map(str, self.block))}\n}}"

@dataclass
class FunctionCall():
    name: str
    args: list

    def __str__(self):
        return f"{self.name}({', '.join(map(str, self.args))})"

# EXPRESSIONS

@dataclass
class Or(Expression):
    left: Expression
    right: Expression

    def __str__(self):
        return f"{self.left} or {self.right}"

@dataclass
class And(Expression):
    left: Expression
    right: Expression

    def __str__(self):
        return f"{self.left} and {self.right}"

@dataclass
class Equal(Expression):
    left: Expression
    right: Expression

    def __str__(self):
        return f"{self.left} = {self.right}"

@dataclass
class NotEqual(Expression):
    left: Expression
    right: Expression

    def __str__(self):
        return f"{self.left} != {self.right}"

@dataclass
class LessThan(Expression):
    left: Expression
    right: Expression

    def __str__(self):
        return f"{self.left} < {self.right}"

@dataclass
class GreaterThan(Expression):
    left: Expression
    right: Expression

    def __str__(self):
        return f"{self.left} > {self.right}"

@dataclass
class LessThanOrEqual(Expression):
    left: Expression
    right: Expression

    def __str__(self):
        return f"{self.left} <= {self.right}"

@dataclass
class GreaterThanOrEqual(Expression):
    left: Expression
    right: Expression

    def __str__(self):
        return f"{self.left} >= {self.right}"

@dataclass
class Add(Expression):
    left: Expression
    right: Expression

    def __str__(self):
        return f"{self.left} + {self.right}"

@dataclass
class Sub(Expression):
    left: Expression
    right: Expression

    def __str__(self):
        return f"{self.left} - {self.right}"

@dataclass
class Power(Expression):
    left: Expression
    right: Expression

    def __str__(self):
        return f"{self.left} ^ {self.right}"

@dataclass
class Mul(Expression):
    left: Expression
    right: Expression

    def __str__(self):
        return f"{self.left} * {self.right}"

@dataclass
class Div(Expression):
    left: Expression
    right: Expression

    def __str__(self):
        return f"{self.left} / {self.right}"

@dataclass
class Mod(Expression):
    left: Expression
    right: Expression

    def __str__(self):
        return f"{self.left} % {self.right}"

@dataclass
class UnaryMinus(Expression):
    expr: Expression

    def __str__(self):
        return f"-{self.expr}"

@dataclass
class LogicNot(Expression):
    expr: Expression

    def __str__(self):
        return f"not {self.expr}"

@dataclass
class ArrayAccess(Expression):
    name: str
    indexes: list[Expression]

    def __str__(self):
        return f"{self.name}{''.join(map(lambda i: f"[{i}]", self.indexes))}"

@dataclass
class Id(Expression):
    name: str

    def __str__(self):
        return self.name

@dataclass
class IntLit(Expression):
    value: int

    def __str__(self):
        return str(self.value)
    

@dataclass
class FloatLit(Expression):
    value: float

    def __str__(self):
        return str(self.value)

@dataclass
class BooleanLit(Expression):
    value: bool

    def __str__(self):
        return str(self.value)

@dataclass
class String(Expression):
    value: str

    def __str__(self):
        return f'"{self.value}"'

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
