from __future__ import annotations

import torch


def to_significant_figures(x: float | int, sf: int = 3) -> str:
    """
    Get a string representation of a float, rounded to
    `sf` significant figures.
    """

    # do the actual rounding
    possibly_scientific = f"{x:.{sf}g}"

    # this might be in e.g. 1.23e+02 format,
    # so convert to float and back to string
    return f"{float(possibly_scientific):g}"


def index_last_dim(tensor: torch.Tensor, i: int) -> torch.Tensor:
    """
    Get `tensor[..., [i]]` in a TorchScript-compatible way.
    """

    # to do this:
    # 1. transpose first and last dimensions
    # 2. index last dimension
    # 3. transpose back

    # need to ensure that the tensor is > 1 dim for this to work
    if tensor.dim() == 1:
        return tensor[[i]]
    
    return tensor.transpose(-1, 0)[[i]].transpose(-1, 0)
