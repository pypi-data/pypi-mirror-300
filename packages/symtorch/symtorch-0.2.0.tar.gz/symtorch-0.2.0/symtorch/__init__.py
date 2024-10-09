from __future__ import annotations

from typing import cast

import sympy
import torch
from torch.types import Number

from .operations import Id, get_torch_equivalent
from .symbolic_module import Expression, Parameter, Symbol
from .utils import index_last_dim

__all__ = ["symtorchify", "SymbolicExpression", "SymbolAssignment"]
__version__ = "0.2.0"


def symtorchify(
    expr: str | sympy.Basic | Number,
    trainable: bool = True,
    trainable_ints: bool = False,
) -> Expression:
    """
    Convert a string, SymPy object, or numeric value to a vanilla
    PyTorch implementation of the expression.

    Parameters
    ----------
    expr
        The expression or value to convert.
    trainable
        Whether the resulting parameters should be trainable, by default True.
    trainable_ints
        Whether integer parameters should be trainable, by default False. Sympy
        converts e.g. the division operator into a combination of a
        multiplication and an exponentiation operator:

        .. math::

            a / b = a * b^{-1}

        The `-1` exponent is converted to a :class:`symtorch.Parameter` by
        ``symtorch``. If ``trainable_ints`` is ``True``, this exponent will be
        trainable (and hence e.g. :math:`a/b` may change during training to be:

        .. math::

            a * (b^{-1.56})

    Returns
    -------
    Expression
        The converted SymTorch Expression.

    Raises
    ------
    ValueError
        If ``trainable_ints`` is ``True`` but ``trainable`` is ``False``.

    Examples
    --------
    Create a simple addition of two symbols:

    >>> model = symtorchify("x + y")
    >>> model.long_hand_representation()
    Expression(Add, [Symbol('x'), Symbol('y')])
    >>> str(model)
    >>> x + y
    >>> len(list(model.parameters()))
    0
    >>> input = {"x": torch.scalar_tensor(1), "y": torch.scalar_tensor(2)}
    >>> model(input)
    tensor([3.])
    """
    if trainable_ints and not trainable:
        raise ValueError("`trainable` must be True if `trainable_ints` is True")

    actual_expr = (
        sympy.sympify(expr) if not isinstance(expr, sympy.Basic) else expr
    )

    if isinstance(actual_expr, sympy.Symbol):
        symbol = Symbol(str(actual_expr))
        return Expression(operation=Id(), nodes=[symbol])

    if isinstance(actual_expr, (sympy.Number, sympy.NumberSymbol)):
        if actual_expr.is_integer and not trainable_ints:  # type: ignore
            param = Parameter(int(actual_expr), trainable=False)
        else:
            param = Parameter(float(actual_expr), trainable)
        return Expression(operation=Id(), nodes=[param])

    actual_expr = cast(sympy.Expr, actual_expr)
    torch_op = get_torch_equivalent(actual_expr)

    args = [
        symtorchify(arg, trainable=trainable, trainable_ints=trainable_ints)
        for arg in actual_expr.args
    ]

    return Expression(
        torch_op,
        args,
        trainable=trainable,
        trainable_ints=trainable_ints,
    )


def SymbolicExpression() -> Expression:
    """
    Create an empty, place-holder :class:`Expression`.

    Returns
    -------
    Expression
        An empty Expression.

    Examples
    --------
    Use this as a placeholder for a model:

    >>> model = SymbolicExpression()
    >>> model
    empty

    Fill it with a symbolic expression later:

    >>> other_model = symtorchify("x + 2.0", trainable=False)
    >>> model.load_state_dict(other_model.state_dict())
    >>> model
    x + 2.0
    """
    return Expression(operation=Id(), nodes=[Symbol("empty")])


class SymbolAssignment(torch.nn.Module):
    """
    Convert a tensor into a dictionary of symbols.

    This module converts a tensor ``X`` of shape ``(..., N)`` into a dictionary
    of symbols, ``{s: X[..., [i]]}``, where ``s`` is the ``i``'th symbol in
    `symbol_order`.

    Parameters
    ----------
    symbol_order
        The order of symbols to use for assignment, by default None.

    Examples
    --------
    Use a :class:`SymbolAssignment` module in combination with a
    :class:`~symtorch.SymbolicExpression` within a :class:`torch.nn.Sequential`
    module to create a simple model:

    >>> model = torch.nn.Sequential(
    ...     SymbolAssignment(["x", "y"]),
    ...     symtorchify("x**2 + 2*y")
    ... )
    >>> input = torch.arange(10).reshape(5, 2)
    >>> model(input)
    tensor([[ 2],
            [10],
            [26],
            [50],
            [82]])
    """

    def __init__(
        self,
        symbol_order: list[str] | None = None,
    ):
        super().__init__()
        self.symbol_order = symbol_order

    def forward(self, X: torch.Tensor):
        """
        Convert the input tensor to a dictionary of symbols.

        Parameters
        ----------
        X
            Input tensor of shape ``(..., N)``.

        Returns
        -------
        dict
            A dictionary mapping symbol names to tensor slices.

        Raises
        ------
        ValueError
            If ``symbol_order`` is not set before calling this method.
        """
        if self.symbol_order is None:
            raise ValueError(
                "SymbolAssignment must be given a symbol_order "
                "before it can be used"
            )
        symbol_dict = {
            s: index_last_dim(X, i) for i, s in enumerate(self.symbol_order)
        }
        return symbol_dict

    def __repr__(self):
        return f"SymbolAssignment({self.symbol_order})"

    def get_extra_state(self) -> list[str] | None:
        return self.symbol_order

    def set_extra_state(self, symbol_order: list[str] | None):
        self.symbol_order = symbol_order
