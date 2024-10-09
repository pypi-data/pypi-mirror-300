<div align="center">
<img src="https://raw.githubusercontent.com/jla-gardner/symtorch/main/docs/source/_static/icon-with-text.svg" style="width: min(100%, 400px); height: auto;"/>
</div>

---

Fast, optimisable, symbolic expressions in PyTorch.

```python-repl
>>> from symtorch import symtorchify
>>> f = symtorchify("x**2 + 2.5*x + 1.7")
>>> f
x²+2.5x+1.7
>>> f({"x": torch.tensor(2.0)})
tensor([10.7000], grad_fn=<AddBackward0>)
```

## Installation

```bash
pip install symtorch
```

## Features

- Symbolic expressions with PyTorch integration
- Automatic differentiation and optimization
- Compatible with TorchScript
- Easy saving and loading via PyTorch's native mechanisms
- Seamless integration with existing PyTorch models

For detailed documentation and examples, visit our [Documentation](https://jla-gardner.github.io/symtorch/).
