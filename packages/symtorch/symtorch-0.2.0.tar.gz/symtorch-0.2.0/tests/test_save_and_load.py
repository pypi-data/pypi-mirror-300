from __future__ import annotations

from pathlib import Path

import torch

from symtorch import SymbolAssignment, SymbolicExpression, symtorchify
from symtorch.symbolic_module import Expression, ExpressionState


def test_state_dict():
    model = symtorchify("abs(a) + sin(2 + b)")

    # this is definitely a nested Expression
    assert isinstance(model.nodes[0], Expression)

    # despite the nesting, the state dict should only contain
    # a single entry: _extra_state
    state_dict = model.state_dict()
    assert len(state_dict) == 1
    assert "_extra_state" in state_dict
    assert isinstance(state_dict["_extra_state"], ExpressionState)

    empty_model = SymbolicExpression()
    empty_model.load_state_dict(state_dict)

    input = {"a": torch.tensor([1.0]), "b": torch.tensor([2.0])}
    assert torch.allclose(model(input), empty_model(input))


def test_save_and_load(tmpdir: Path):
    model = symtorchify("abs(a) + sin(2 + b)")

    file = str(tmpdir / "test_save_and_load.pt")
    torch.save(model, file)
    new_model = torch.load(file)

    input = {"a": torch.tensor([1.0]), "b": torch.tensor([2.0])}
    assert torch.allclose(model(input), new_model(input))


def test_torchscript(tmpdir: Path):
    model = symtorchify("abs(a) + sin(2 + b)")

    file = str(tmpdir / "test_torchscript.pt")
    scripted_model = torch.jit.script(model)
    torch.jit.save(scripted_model, file)
    new_model = torch.jit.load(file)

    input = {"a": torch.tensor([1.0]), "b": torch.tensor([2.0])}
    assert torch.allclose(model(input), new_model(input))


def test_assignment():
    model = torch.nn.Sequential(
        SymbolAssignment(["x", "y"]),
        symtorchify("x**2 + 2*y"),
    )
    input = torch.arange(10).reshape(5, 2)

    empty_model = torch.nn.Sequential(SymbolAssignment(), SymbolicExpression())
    empty_model.load_state_dict(model.state_dict())
    assert empty_model[0].symbol_order == ["x", "y"]

    assert torch.allclose(model(input), empty_model(input))
