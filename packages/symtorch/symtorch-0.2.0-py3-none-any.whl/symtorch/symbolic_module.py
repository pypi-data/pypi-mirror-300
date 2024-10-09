from __future__ import annotations

from abc import ABC, abstractmethod
from typing import NamedTuple, Sequence

import sympy
import torch
from torch.nn.modules.module import _EXTRA_STATE_KEY_SUFFIX
from torch.types import Number

from .operations import Operation
from .utils import to_significant_figures

# State Dict Logic for SymbolicModule and its subclasses:
#
# 1. PyTorch creates and reloads state dicts in a top-down fashion
#    (parents first, then children, then grandchildren, etc.).
#
# 2. To allow loading of arbitrary equations into an empty Expression:
#    - The topmost Expression object saves and loads the entire
#      expression as a string.
#    - Child SymbolicModules (Symbol, Parameter) don't save or load
#      anything individually.
#    - Their state is captured by the topmost Expression object.
#
# 3. Custom logic in Expression class:
#    - get_extra_state: Saves the expression, trainable, and
#      trainable_ints flags.
#    - set_extra_state: Reconstructs the entire expression tree from
#      the saved string.
#    - _save_to_state_dict: Prevents duplicate saving of nested
#      Expressions.
#    - _load_from_state_dict: Ensures only the topmost Expression is
#      loaded, discarding any nested state.
#
# 4. Symbol and Parameter classes:
#    - Override _save_to_state_dict and _load_from_state_dict to do
#      nothing, as their state is managed by the parent Expression.


class SymbolicModule(torch.nn.Module, ABC):
    """
    An abstract base class for all symbolic modules.
    """

    @abstractmethod
    def forward(self, x: dict[str, torch.Tensor]) -> torch.Tensor:
        """
        Evaluate the symbolic module.
        """
        pass

    @abstractmethod
    def long_hand_representation(self, sig_fig: int | None = 3) -> str:
        """
        Return a long-hand string representation of the symbolic module.
        """
        pass

    def __repr__(self):
        return str(self.sympy())

    def sympy(self, sig_fig: int | None = 3) -> sympy.Basic:
        """
        Return a SymPy expression for the symbolic module.
        """
        raw = self.long_hand_representation(sig_fig)
        return sympy.sympify(raw)

    def _repr_latex_(self):
        return self.sympy()._repr_latex_()


class ExpressionState(NamedTuple):
    expression: str
    trainable: bool
    trainable_ints: bool


class Expression(SymbolicModule):
    """
    A tree-based, PyTorch-compatible implementation of a symbolic
    expression, where each leaf node is a :class:`Symbol` or
    :class:`Parameter`, and each internal node is another
    :class:`Expression`.

    Attributes
    ----------
    operation: Operation
        The operation at the root of the expression tree.
    nodes: Sequence[SymbolicModule]
        The child nodes of the expression tree.
    trainable: bool
        Whether the expression is trainable.
    trainable_ints: bool
        Whether integer parameters in the expression are trainable.
    """

    def __init__(
        self,
        operation: Operation,
        nodes: Sequence[SymbolicModule],
        trainable: bool = True,
        trainable_ints: bool = True,
    ):
        super().__init__()
        self.operation: Operation = operation
        self.nodes = torch.nn.ModuleList(nodes)
        self.trainable = trainable
        self.trainable_ints = trainable_ints

    def forward(self, x: dict[str, torch.Tensor]) -> torch.Tensor:
        input_values = [node(x) for node in self.nodes]
        return self.operation(input_values)

    def long_hand_representation(self, sig_fig: int | None = 3) -> str:
        node_reprs = ", ".join(
            node.long_hand_representation(sig_fig) for node in self.nodes
        )
        return f"{self.operation.__class__.__name__}({node_reprs})"

    ### STATE DICT LOGIC ###

    def get_extra_state(self) -> ExpressionState:
        return ExpressionState(
            expression=repr(self.sympy(sig_fig=None)),
            trainable=self.trainable,
            trainable_ints=self.trainable_ints,
        )

    def set_extra_state(self, state: ExpressionState) -> None:
        from symtorch import symtorchify

        expression, trainable, trainable_ints = state
        symtorch: Expression = symtorchify(
            expression,
            trainable=trainable,
            trainable_ints=trainable_ints,
        )
        self.operation = symtorch.operation
        self.nodes = symtorch.nodes

    def _save_to_state_dict(self, destination, prefix, keep_vars):
        # see above comment for explanation
        for key, state in destination.items():
            if not key.endswith(_EXTRA_STATE_KEY_SUFFIX):
                continue
            actual_key = key.replace(_EXTRA_STATE_KEY_SUFFIX, "")
            if prefix.startswith(actual_key) and isinstance(
                state, ExpressionState
            ):
                return

        destination[prefix + _EXTRA_STATE_KEY_SUFFIX] = self.get_extra_state()

    def _load_from_state_dict(
        self,
        state_dict,
        prefix,
        local_metadata,
        strict,
        missing_keys,
        unexpected_keys,
        error_msgs,
    ):
        # see above comment for explanation
        key = prefix + _EXTRA_STATE_KEY_SUFFIX
        for other_key in list(state_dict.keys()):
            if key != other_key and other_key.startswith(prefix):
                del state_dict[other_key]

        if key in state_dict:
            self.set_extra_state(state_dict[key])


class Symbol(SymbolicModule):
    """
    A symbolic variable, i.e. a leaf node in the expression tree.

    Attributes
    ----------
    name: str
        The name of the symbol.
    """

    def __init__(self, name: str):
        super().__init__()
        self.name = name

    def forward(self, x: dict[str, torch.Tensor]) -> torch.Tensor:
        return x[self.name]

    def long_hand_representation(self, sig_fig: int | None = 3) -> str:
        return self.name

    ### STATE DICT LOGIC ###

    def _save_to_state_dict(self, *args, **kwargs):
        pass

    def _load_from_state_dict(self, *args, **kwargs):
        pass


class Parameter(SymbolicModule):
    """
    A symbolic parameter, i.e. a leaf node in the expression tree.

    Attributes
    ----------
    param: torch.nn.Parameter
        The underlying value of the parameter.
    """

    def __init__(self, value: Number, trainable: bool = True):
        super().__init__()
        if trainable:
            self.param = torch.nn.Parameter(
                torch.tensor(float(value)), requires_grad=True
            )
        else:
            self.param = torch.nn.Parameter(
                torch.tensor(value), requires_grad=False
            )

    def forward(self, x: dict[str, torch.Tensor]) -> torch.Tensor:
        return self.param

    def long_hand_representation(self, sig_fig: int | None = 3) -> str:
        value = self.param.item()
        if sig_fig is not None:
            value = to_significant_figures(value, sig_fig)
        return str(value)

    ### STATE DICT LOGIC ###

    def _save_to_state_dict(self, *args, **kwargs):
        pass

    def _load_from_state_dict(self, *args, **kwargs):
        pass
