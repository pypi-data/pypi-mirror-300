from __future__ import annotations

import pytest
import torch

from symtorch import SymbolicExpression, symtorchify
from symtorch.operations import (
    BinaryOperation,
    Operation,
    ReductionOperation,
    UnaryOperation,
    _sympy_to_torch,
    get_torch_equivalent,
    im,
)

ALL_OPERATIONS = list(_sympy_to_torch.values())


@pytest.mark.parametrize("op_type", ALL_OPERATIONS)
def test_torchscript(op_type: type[Operation]):
    op = op_type()
    ts_op = torch.jit.script(op)
    assert isinstance(ts_op, torch.jit.ScriptModule)

    # get a tensor that should not break anything
    dtype = torch.complex64 if isinstance(op, im) else torch.float64
    inoffensive_tensor = torch.tensor([0.1, 0.2, 0.3], dtype=dtype)

    if isinstance(op, UnaryOperation):
        assert torch.allclose(
            ts_op([inoffensive_tensor]),
            op([inoffensive_tensor]),
            equal_nan=True,
        )

    elif isinstance(op, BinaryOperation):
        assert torch.allclose(
            ts_op([inoffensive_tensor, inoffensive_tensor]),
            op([inoffensive_tensor, inoffensive_tensor]),
            equal_nan=True,
        )

    elif isinstance(op, ReductionOperation):
        assert torch.allclose(
            ts_op([inoffensive_tensor]),
            op([inoffensive_tensor]),
            equal_nan=True,
        )


def test_graceful_failure():
    with pytest.raises(
        ValueError, match="Expressions of type.*are not .*supported"
    ):
        get_torch_equivalent(None)  # type: ignore


@pytest.mark.parametrize(
    "expression,input_dict,expected",
    [
        (
            "a + b",
            {
                "a": torch.tensor([0.1, 0.2, 0.3]),
                "b": torch.tensor([0.4, 0.5, 0.6]),
            },
            torch.tensor([0.5, 0.7, 0.9]),
        ),
        (
            "a * b",
            {
                "a": torch.tensor([0.1, 0.2, 0.3]),
                "b": torch.tensor([0.4, 0.5, 0.6]),
            },
            torch.tensor([0.04, 0.1, 0.18]),
        ),
        (
            "a ** b",
            {
                "a": torch.tensor([2.0, 3.0, 4.0]),
                "b": torch.tensor([2.0, 3.0, 2.0]),
            },
            torch.tensor([4.0, 27.0, 16.0]),
        ),
        (
            "exp(a)",
            {"a": torch.tensor([0.1, 0.2, 0.3])},
            torch.exp(torch.tensor([0.1, 0.2, 0.3])),
        ),
        (
            "log(a)",
            {"a": torch.tensor([1.1, 2.2, 3.3])},
            torch.log(torch.tensor([1.1, 2.2, 3.3])),
        ),
        (
            "sin(a)",
            {"a": torch.tensor([0.1, 0.2, 0.3])},
            torch.sin(torch.tensor([0.1, 0.2, 0.3])),
        ),
        (
            "acos(a)",
            {"a": torch.tensor([0.1, 0.2, 0.3])},
            torch.acos(torch.tensor([0.1, 0.2, 0.3])),
        ),
        (
            "cos(a)",
            {"a": torch.tensor([0.1, 0.2, 0.3])},
            torch.cos(torch.tensor([0.1, 0.2, 0.3])),
        ),
        (
            "asin(a)",
            {"a": torch.tensor([0.1, 0.2, 0.3])},
            torch.asin(torch.tensor([0.1, 0.2, 0.3])),
        ),
        (
            "tan(a)",
            {"a": torch.tensor([0.1, 0.2, 0.3])},
            torch.tan(torch.tensor([0.1, 0.2, 0.3])),
        ),
        (
            "atan(a)",
            {"a": torch.tensor([0.1, 0.2, 0.3])},
            torch.atan(torch.tensor([0.1, 0.2, 0.3])),
        ),
        (
            "atan2(a, b)",
            {
                "a": torch.tensor([0.1, 0.2, 0.3]),
                "b": torch.tensor([0.4, 0.5, 0.6]),
            },
            torch.atan2(
                torch.tensor([0.1, 0.2, 0.3]), torch.tensor([0.4, 0.5, 0.6])
            ),
        ),
        (
            "sinh(a)",
            {"a": torch.tensor([0.1, 0.2, 0.3])},
            torch.sinh(torch.tensor([0.1, 0.2, 0.3])),
        ),
        (
            "asinh(a)",
            {"a": torch.tensor([0.1, 0.2, 0.3])},
            torch.asinh(torch.tensor([0.1, 0.2, 0.3])),
        ),
        (
            "cosh(a)",
            {"a": torch.tensor([0.1, 0.2, 0.3])},
            torch.cosh(torch.tensor([0.1, 0.2, 0.3])),
        ),
        (
            "acosh(a)",
            {"a": torch.tensor([1.1, 1.2, 1.3])},
            torch.acosh(torch.tensor([1.1, 1.2, 1.3])),
        ),
        (
            "tanh(a)",
            {"a": torch.tensor([0.1, 0.2, 0.3])},
            torch.tanh(torch.tensor([0.1, 0.2, 0.3])),
        ),
        (
            "atanh(a)",
            {"a": torch.tensor([0.1, 0.2, 0.3])},
            torch.atanh(torch.tensor([0.1, 0.2, 0.3])),
        ),
        (
            "re(a)",
            {"a": torch.tensor([1 + 2j, 3 + 4j, 5 + 6j])},
            torch.real(torch.tensor([1 + 2j, 3 + 4j, 5 + 6j])),
        ),
        (
            "im(a)",
            {"a": torch.tensor([1 + 2j, 3 + 4j, 5 + 6j])},
            torch.imag(torch.tensor([1 + 2j, 3 + 4j, 5 + 6j])),
        ),
        (
            "abs(a)",
            {"a": torch.tensor([-0.1, 0.2, -0.3])},
            torch.abs(torch.tensor([-0.1, 0.2, -0.3])),
        ),
        (
            "max(a, b, c)",
            {
                "a": torch.tensor([0.1, 0.2, 0.3]),
                "b": torch.tensor([0.4, 0.1, 0.2]),
                "c": torch.tensor([0.2, 0.3, 0.1]),
            },
            torch.max(
                torch.max(
                    torch.tensor([0.1, 0.2, 0.3]), torch.tensor([0.4, 0.1, 0.2])
                ),
                torch.tensor([0.2, 0.3, 0.1]),
            ),
        ),
        (
            "min(a, b, c)",
            {
                "a": torch.tensor([0.1, 0.2, 0.3]),
                "b": torch.tensor([0.4, 0.1, 0.2]),
                "c": torch.tensor([0.2, 0.3, 0.1]),
            },
            torch.min(
                torch.min(
                    torch.tensor([0.1, 0.2, 0.3]), torch.tensor([0.4, 0.1, 0.2])
                ),
                torch.tensor([0.2, 0.3, 0.1]),
            ),
        ),
    ],
)
def test_operations(
    expression: str,
    input_dict: dict[str, torch.Tensor],
    expected: torch.Tensor,
):
    expr = symtorchify(expression)
    assert torch.allclose(expr(input_dict), expected)

    empty_expr = SymbolicExpression()
    empty_expr.load_state_dict(expr.state_dict())
    assert torch.allclose(empty_expr(input_dict), expected)
