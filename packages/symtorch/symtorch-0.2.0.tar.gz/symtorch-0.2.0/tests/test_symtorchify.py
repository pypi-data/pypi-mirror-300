import pytest

import symtorch.operations
from symtorch import symtorchify
from symtorch.symbolic_module import Expression


def test_basic():
    expression = symtorchify("x + y")
    assert isinstance(expression, Expression)
    assert str(expression) == "x + y"


@pytest.mark.parametrize("trainable", [True, False])
def test_trainability(trainable: bool):
    expression = symtorchify("x + 2.0", trainable=trainable)
    assert isinstance(expression, Expression)
    assert expression.trainable == trainable

    trainable_params = [p for p in expression.parameters() if p.requires_grad]
    assert len(trainable_params) == (1 if trainable else 0)


@pytest.mark.parametrize("trainable_ints", [True, False])
def test_trainable_ints(trainable_ints: bool):
    expression = symtorchify("x + 2", trainable_ints=trainable_ints)
    assert isinstance(expression, Expression)
    assert expression.trainable_ints == trainable_ints
    assert list(expression.parameters())[0].requires_grad == trainable_ints

    # this should carry over to strange lack of division in sympy
    expression = symtorchify("1 / x", trainable_ints=trainable_ints)
    assert isinstance(expression.operation, symtorch.operations.Pow)
    assert list(expression.parameters())[0].requires_grad == trainable_ints
