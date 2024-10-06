from __future__ import annotations
from typing import Generic, Tuple
import torch
from activeft.acquisition_functions import M, AcquisitionFunction, Targeted
from activeft.acquisition_functions.undirected_vtl import UndirectedVTL
from activeft.acquisition_functions.vtl import VTL
from activeft.data import Dataset
from activeft.utils import (
    DEFAULT_EMBEDDING_BATCH_SIZE,
    DEFAULT_MINI_BATCH_SIZE,
    DEFAULT_NUM_WORKERS,
    DEFAULT_SUBSAMPLE,
)


class ActiveDataLoader(Generic[M]):
    r"""
    `ActiveDataLoader` can be used as a drop-in replacement for random data selection or nearest neighbor retrieval:

    ```python
    data_loader = ActiveDataLoader.initialize(dataset, target, batch_size=64)
    batch = dataset[data_loader.next(model)]
    ```

    where
    - `model` is a PyTorch `nn.Module`,
    - `dataset` is a dataset of inputs (where `dataset[i]` returns a vector of length $d$), and
    - `target` is a tensor of prediction targets (shape $m \times d$) or `None`.

    If `dataset` already includes pre-computed embeddings, `model` can be omitted:

    ```python
    data_loader = ActiveDataLoader.initialize(dataset, target, batch_size=64)
    batch = dataset[data_loader.next()]
    ```

    The target can also be updated sequentially:

    ```python
    data_loader = ActiveDataLoader.initialize(dataset, target=None, batch_size=64, force_targeted=True)
    for target in targets:
        batch = dataset[data_loader.with_target(target).next(model)]
    ```
    """

    dataset: Dataset
    r"""Inputs (shape $n \times d$) to be selected from."""

    batch_size: int
    r"""Size of the batch to be selected."""

    acquisition_function: AcquisitionFunction[M]
    r"""Acquisition function to be used for data selection."""

    device: torch.device | None = None
    r"""Device used for computation of the acquisition function."""

    def __init__(
        self,
        dataset: Dataset,
        batch_size: int,
        acquisition_function: AcquisitionFunction[M],
        device: torch.device | None = None,
    ):
        """
        Explicitly constructs an active data loader with a custom acquisition function.
        `activeft` supports a wide range of acquisition functions which are summarized in `activeft.acquisition_functions`.
        """

        assert len(dataset) > 0, "Data must be non-empty"
        assert batch_size > 0, "Batch size must be positive"

        self.dataset = dataset
        self.batch_size = batch_size
        self.acquisition_function = acquisition_function
        self.device = device

    @classmethod
    def initialize(
        cls,
        dataset: Dataset,
        target: torch.Tensor | None,
        batch_size: int,
        device: torch.device | None = None,
        subsampled_target_frac: float = 1,
        max_target_size: int | None = None,
        mini_batch_size: int = DEFAULT_MINI_BATCH_SIZE,
        embedding_batch_size: int = DEFAULT_EMBEDDING_BATCH_SIZE,
        num_workers: int = DEFAULT_NUM_WORKERS,
        subsample_acquisition: bool = DEFAULT_SUBSAMPLE,
        force_targeted: bool = False,
    ):
        r"""
        Initializes an active data loader.

        :param dataset: Inputs (shape $n \times d$) to be selected from.
        :param target: Tensor of prediction targets (shape $m \times d$) or `None`.
        :param batch_size: Size of the batch to be selected.
        :param device: Device used for computation of the acquisition function.
        :param subsampled_target_frac: Fraction of the target to be subsampled in each iteration. Must be in $(0,1]$. Default is $1$. Ignored if `target` is `None`.
        :param max_target_size: Maximum size of the target to be subsampled in each iteration. Default is `None` in which case the target may be arbitrarily large. Ignored if `target` is `None`.
        :param mini_batch_size: Size of mini batches used for computing the acquisition function.
        :param embedding_batch_size: Batch size used for computing the embeddings.
        :param num_workers: Number of workers used for data loading.
        :param subsample_acquisition: Whether to subsample the data to a single mini batch before computing the acquisition function.
        :param force_targeted: Whether to force targeted data selection. If `True`, `target` must be provided subsequently using `with_target`.
        """

        if target is not None or force_targeted:
            acquisition_function = VTL(
                target=target if target is not None else torch.tensor([]),
                subsampled_target_frac=subsampled_target_frac,
                max_target_size=max_target_size,
                mini_batch_size=mini_batch_size,
                embedding_batch_size=embedding_batch_size,
                num_workers=num_workers,
                subsample=subsample_acquisition,
            )
        else:
            acquisition_function = UndirectedVTL(
                mini_batch_size=mini_batch_size,
                embedding_batch_size=embedding_batch_size,
                num_workers=num_workers,
                subsample=subsample_acquisition,
            )
        return cls(
            dataset=dataset,
            batch_size=batch_size,
            acquisition_function=acquisition_function,  # type: ignore
            device=device,
        )

    def next(self, model: M | None = None) -> Tuple[torch.Tensor, torch.Tensor]:
        r"""
        Selects the next batch of data provided a `model` which is a PyTorch `nn.Module`.

        .. warning::

            The computational complexity of `next` scales cubically with the size of the target. If the target is large, it is recommended to set `max_target_size` to value other than `None`.

        :param model: Model to be used for data selection. For embedding-based acquisition functions, `model` can be `None` in which case the data is treated as if it was already embedded.
        :return: Indices of the selected data and corresponding value of the acquisition function in the format `(indices, values)`.
        """

        return self.acquisition_function.select(
            batch_size=self.batch_size,
            model=model,  # type: ignore
            dataset=self.dataset,
            device=self.device,
        )

    def with_target(self, target: torch.Tensor) -> ActiveDataLoader[M]:
        r"""
        Returns the active data loader with a new target.

        :param target: Tensor of prediction targets (shape $m \times d$).
        :return: Updated active data loader.
        """

        assert isinstance(
            self.acquisition_function, Targeted
        ), "Acquisition function must be targeted"
        self.acquisition_function.set_target(target)
        return self
