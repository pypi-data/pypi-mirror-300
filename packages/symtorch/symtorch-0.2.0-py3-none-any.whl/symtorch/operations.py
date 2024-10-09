from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Callable

import sympy
import torch
from torch.types import Number


class Operation(torch.nn.Module, ABC):
    """
    Abstract base class for all ``torch`` equivalents of SymPy operations.
    """

    @abstractmethod
    def forward(self, x: list[torch.Tensor]) -> torch.Tensor:
        """
        Forward passes of ``Operations`` adhere to the same interface:
        accepting a list of ``torch.Tensor`` objects and returning a single
        ``torch.Tensor``.
        """
        pass


class Id(Operation):
    """Identity operation."""

    def forward(self, x: list[torch.Tensor]) -> torch.Tensor:
        assert len(x) == 1
        return x[0]


class UnaryOperation(Operation, ABC):
    """
    ABC for all ``torch`` equivalents of SymPy unary operations.
    """

    def __init__(
        self,
        torch_unary_op: Callable[[torch.Tensor], torch.Tensor],
    ):
        super().__init__()
        self.torch_unary_op = torch_unary_op

    def forward(self, x: list[torch.Tensor]) -> torch.Tensor:
        assert len(x) == 1
        return self.torch_unary_op(x[0])


class BinaryOperation(Operation, ABC):
    """
    ABC for all ``torch`` equivalents of SymPy binary operations.
    """

    def __init__(
        self,
        torch_binary_op: Callable[[torch.Tensor, torch.Tensor], torch.Tensor],
    ):
        super().__init__()
        self.torch_binary_op = torch_binary_op

    def forward(self, x: list[torch.Tensor]) -> torch.Tensor:
        assert len(x) == 2
        return self.torch_binary_op(x[0], x[1])


class ReductionOperation(Operation, ABC):
    """
    ABC for all ``torch`` equivalents of SymPy operations that act to 
    reduce a variable number of inputs using the same operation. 
    Examples include addition and multiplication.
    """

    def __init__(
        self,
        torch_binary_op: Callable[[torch.Tensor, torch.Tensor], torch.Tensor],
        default_value: Number,
    ):
        super().__init__()
        self.torch_binary_op = torch_binary_op
        self.default_value = default_value

    def forward(self, x: list[torch.Tensor]) -> torch.Tensor:
        starting_value = torch.tensor([self.default_value], device=x[0].device)
        for tensor in x:
            starting_value = self.torch_binary_op(starting_value, tensor)
        return starting_value


_sympy_to_torch: dict[type[sympy.Expr], type[Operation]] = {}


def register(sympy_type: type[sympy.Expr]):
    def decorator(torch_type: type[Operation]):
        _sympy_to_torch[sympy_type] = torch_type
        return torch_type

    return decorator


def get_torch_equivalent(expr: sympy.Expr) -> Operation:
    if type(expr) not in _sympy_to_torch:
        raise ValueError(
            f"Expressions of type {type(expr)} are not (yet) supported"
        )
    return _sympy_to_torch[type(expr)]()


### Sympy-to-Torch Equivalents ###
# we give the operations names that are identical the
# sympy equivalents so as to make flipping between the
# two as obvious as possible


@register(sympy.Add)
class Add(ReductionOperation):
    def __init__(self):
        super().__init__(torch.add, 0)


@register(sympy.Mul)
class Mul(ReductionOperation):
    def __init__(self):
        super().__init__(torch.mul, 1)


@register(sympy.Pow)
class Pow(BinaryOperation):
    def __init__(self):
        super().__init__(torch.pow)


@register(sympy.exp)
class exp(UnaryOperation):
    def __init__(self):
        super().__init__(torch.exp)


@register(sympy.log)
class log(UnaryOperation):
    def __init__(self):
        super().__init__(torch.log)


# Trigonometric functions
@register(sympy.sin)
class sin(UnaryOperation):
    def __init__(self):
        super().__init__(torch.sin)


@register(sympy.acos)
class acos(UnaryOperation):
    def __init__(self):
        super().__init__(torch.acos)


@register(sympy.cos)
class cos(UnaryOperation):
    def __init__(self):
        super().__init__(torch.cos)


@register(sympy.asin)
class asin(UnaryOperation):
    def __init__(self):
        super().__init__(torch.asin)


@register(sympy.tan)
class tan(UnaryOperation):
    def __init__(self):
        super().__init__(torch.tan)


@register(sympy.atan)
class atan(UnaryOperation):
    def __init__(self):
        super().__init__(torch.atan)


@register(sympy.atan2)
class atan2(BinaryOperation):
    def __init__(self):
        super().__init__(torch.atan2)


# Hyperbolic functions
@register(sympy.sinh)
class sinh(UnaryOperation):
    def __init__(self):
        super().__init__(torch.sinh)


@register(sympy.asinh)
class asinh(UnaryOperation):
    def __init__(self):
        super().__init__(torch.asinh)


@register(sympy.cosh)
class cosh(UnaryOperation):
    def __init__(self):
        super().__init__(torch.cosh)


@register(sympy.acosh)
class acosh(UnaryOperation):
    def __init__(self):
        super().__init__(torch.acosh)


@register(sympy.tanh)
class tanh(UnaryOperation):
    def __init__(self):
        super().__init__(torch.tanh)


@register(sympy.atanh)
class atanh(UnaryOperation):
    def __init__(self):
        super().__init__(torch.atanh)


# Complex functions
@register(sympy.re)
class re(UnaryOperation):
    def __init__(self):
        super().__init__(torch.real)


@register(sympy.im)
class im(UnaryOperation):
    def __init__(self):
        super().__init__(torch.imag)


# Miscellaneous
@register(sympy.Abs)
class abs(UnaryOperation):
    def __init__(self):
        super().__init__(torch.abs)


@register(sympy.Max)
class max(ReductionOperation):
    def __init__(self):
        super().__init__(torch.max, -float("inf"))


@register(sympy.Min)
class min(ReductionOperation):
    def __init__(self):
        super().__init__(torch.min, float("inf"))
