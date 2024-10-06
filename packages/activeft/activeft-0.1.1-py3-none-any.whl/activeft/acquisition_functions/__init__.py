"""
`activeft` supports a wide range of acquisition functions which are summarized here.
The default implementation uses [VTL](acquisition_functions/vtl).
You can use a custom acquisition function as follows:

```python
from activeft.acquisition_functions.undirected_vtl import UndirectedVTL

acquisition_function = UndirectedVTL()
data_loader = activeft.ActiveDataLoader(data, batch_size=64, acquisition_function=acquisition_function)
```

## Overview of Acquisition Functions

The following table provides an overview of the acquisition functions and their properties:

|                                                                    | Relevance? | Diversity? | Model Requirement   |
|--------------------------------------------------------------------|------------|------------|---------------------|
| [ITL](acquisition_functions/itl)                                   | ✅          | ✅          | embedding / kernel  |
| [VTL](acquisition_functions/vtl)                                   | ✅          | ✅          | embedding / kernel  |
| [MMITL](acquisition_functions/mmitl)                               | ✅          | ✅          | embedding / kernel  |
| [CTL](acquisition_functions/ctl)                                   | (✅)        | ✅          | embedding / kernel  |
| [Cosine Similarity](acquisition_functions/cosine_similarity)       | (✅)        | ❌          | embedding           |
| [Undirected ITL](acquisition_functions/undirected_itl)             | ❌          | ✅          | embedding / kernel  |
| [Undirected VTL](acquisition_functions/undirected_vtl)             | ❌          | ✅          | embedding / kernel  |
| [MaxDist](acquisition_functions/max_dist)                          | ❌          | ✅          | embedding / kernel  |
| [k-means++](acquisition_functions/kmeans_pp)                       | ❌          | ✅          | embedding / kernel  |
| [Uncertainty Sampling](acquisition_functions/uncertainty_sampling) | ❌          | ❌          | embedding / kernel  |
| [MinMargin](acquisition_functions/min_margin)                      | ❌          | ❌          | softmax             |
| [MaxEntropy](acquisition_functions/max_entropy)                    | ❌          | ❌          | softmax             |
| [LeastConfidence](acquisition_functions/least_confidence)          | ❌          | ❌          | softmax             |
| [EIG](acquisition_functions/eig)                                   | ✅          | ❌          | embedding / kernel  |
| [Information Density](acquisition_functions/information_density)   | (✅)        | (✅)        | embedding & softmax |
| [Random](acquisition_functions/random)                             | ❌          | (✅)        | -                   |


- **Relevance** captures whether obtained data is "related" to the prediction targets. Methods with checkmarks in parentheses capture some but not all related data.
- **Diversity** captures whether the selected batches are diverse, i.e., whether selected data is non-redundant.
- **Model Requirement** describes the type of model required for the acquisition function. For example, some acquisition functions require an *embedding* or a *kernel* (see activeft.model), while others require the model to output a *softmax* distribution (typically in a classification context).

---
"""

from abc import ABC, abstractmethod
import math
from typing import Callable, Generic, Optional, Tuple, TypeVar
import numpy as np
import torch
from torch.utils.data import DataLoader, Dataset as TorchDataset, Subset
from activeft.data import Dataset
from activeft.model import Model, ModelWithEmbedding
from activeft.utils import (
    DEFAULT_EMBEDDING_BATCH_SIZE,
    DEFAULT_MINI_BATCH_SIZE,
    DEFAULT_NUM_WORKERS,
    DEFAULT_SUBSAMPLE,
    get_device,
    mini_batch_wrapper,
)
import warnings

M = TypeVar("M", bound=Model | None)


class _IndexedDataset(TorchDataset[Tuple[torch.Tensor, int]]):
    def __init__(self, dataset: Dataset):
        self.dataset = dataset

    def __len__(self) -> int:
        return len(self.dataset)

    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, int]:
        data = self.dataset[idx]
        return data, idx


class AcquisitionFunction(ABC, Generic[M]):
    """Abstract base class for acquisition functions."""

    mini_batch_size: int = DEFAULT_MINI_BATCH_SIZE
    """Size of mini batches used for computing the acquisition function."""

    num_workers: int = DEFAULT_NUM_WORKERS
    """Number of workers used for data loading."""

    subsample: bool = DEFAULT_SUBSAMPLE
    """Whether to (uniformly) subsample the data to a single mini batch for faster computation."""

    def __init__(
        self,
        mini_batch_size=DEFAULT_MINI_BATCH_SIZE,
        num_workers=DEFAULT_NUM_WORKERS,
        subsample=DEFAULT_SUBSAMPLE,
    ):
        self.mini_batch_size = mini_batch_size
        self.num_workers = num_workers
        self.subsample = subsample

    @abstractmethod
    def select(
        self,
        batch_size: int,
        model: M,
        dataset: Dataset,
        device: torch.device | None = None,
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        r"""
        Selects the next batch.

        :param batch_size: Size of the batch to be selected. Needs to be smaller than `mini_batch_size`.
        :param model: Model used for data selection.
        :param dataset: Inputs (shape $n \times d$) to be selected from.
        :param device: Device used for computation of the acquisition function.
        :return: Indices of the newly selected batch and corresponding values of the acquisition function.
        """
        pass


class BatchAcquisitionFunction(AcquisitionFunction[M]):
    """
    Abstract base class for acquisition functions that select entire batches with a single computation of the acquisition function.
    """

    @abstractmethod
    def compute(
        self,
        model: M,
        data: torch.Tensor,
        device: torch.device | None = None,
    ) -> torch.Tensor:
        r"""
        Computes the acquisition function for the given data.

        :param model: Model used for data selection.
        :param data: Tensor of inputs (shape $n \times d$) to be selected from.
        :param device: Device used for computation of the acquisition function.
        :return: Acquisition function values for the given data.
        """
        pass

    def select(
        self,
        batch_size: int,
        model: M,
        dataset: Dataset,
        device: torch.device | None = None,
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        return BatchAcquisitionFunction._select(
            compute_fn=self.compute,
            batch_size=batch_size,
            model=model,
            dataset=dataset,
            device=device,
            mini_batch_size=self.mini_batch_size,
            num_workers=self.num_workers,
            subsample=self.subsample,
        )

    @staticmethod
    def _select(
        compute_fn: Callable[[M, torch.Tensor, Optional[torch.device]], torch.Tensor],
        batch_size: int,
        model: M,
        dataset: Dataset,
        device: torch.device | None,
        mini_batch_size: int,
        num_workers: int,
        subsample: bool,
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        indexed_dataset = _IndexedDataset(dataset)
        data_loader = DataLoader(
            indexed_dataset,
            batch_size=mini_batch_size,
            num_workers=num_workers,
            shuffle=True,
        )

        _values = []
        _original_indices = []
        for data, idx in data_loader:
            _values.append(compute_fn(model, data, device))
            _original_indices.append(idx)
            if subsample:
                break
        values = torch.cat(_values)
        original_indices = torch.cat(_original_indices)

        values, indices = torch.topk(values, batch_size)
        return original_indices[indices.cpu()], values.cpu()


State = TypeVar("State")


class SequentialAcquisitionFunction(AcquisitionFunction[M], Generic[M, State]):
    """
    Abstract base class for acquisition functions that select a batch by sequentially adding points.
    """

    force_nonsequential: bool = False
    """Whether to force non-sequential data selection."""

    def __init__(
        self,
        mini_batch_size=DEFAULT_MINI_BATCH_SIZE,
        num_workers=DEFAULT_NUM_WORKERS,
        subsample=DEFAULT_SUBSAMPLE,
        force_nonsequential=False,
    ):
        super().__init__(
            mini_batch_size=mini_batch_size,
            num_workers=num_workers,
            subsample=subsample,
        )
        self.force_nonsequential = force_nonsequential

    @abstractmethod
    def initialize(
        self,
        model: M,
        data: torch.Tensor,
        device: torch.device | None,
    ) -> State:
        r"""
        Initializes the state for batch selection.

        :param model: Model used for data selection.
        :param data: Tensor of inputs (shape $n \times d$) to be selected from.
        :param device: Device used for computation of the acquisition function.
        :return: Initial state of batch selection.
        """
        pass

    @abstractmethod
    def compute(self, state: State) -> torch.Tensor:
        """
        Computes the acquisition function for the given state.

        :param state: State of batch selection.
        :return: Acquisition function values for the given state.
        """
        pass

    @abstractmethod
    def step(self, state: State, i: int) -> State:
        r"""
        Updates the state after adding a data point to the batch.

        :param state: State of batch selection.
        :param i: Index of selected data point.
        :return: Updated state of batch selection.
        """
        pass

    @staticmethod
    def selector(values: torch.Tensor) -> int:
        """
        Given acquisition function values, selects the next data point to be added to the batch.

        :param values: Acquisition function values.
        :return: Index of the selected data point.
        """
        return int(torch.argmax(values).item())

    def select_from_minibatch(
        self, batch_size: int, model: M, data: torch.Tensor, device: torch.device | None
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        r"""
        Selects the next batch from the given mini batch `data`.

        :param batch_size: Size of the batch to be selected. Needs to be smaller than `mini_batch_size`.
        :param model: Model used for data selection.
        :param data: Mini batch of inputs (shape $n \times d$) to be selected from.
        :param device: Device used for computation of the acquisition function.
        :return: Indices of the newly selected batch (with respect to mini batch) and corresponding values of the acquisition function.
        """
        state = self.initialize(model, data, device)

        selected_indices = []
        selected_values = []
        for _ in range(batch_size):
            values = self.compute(state)
            i = self.selector(values)
            selected_indices.append(i)
            selected_values.append(values[i])
            state = self.step(state, i)
        return torch.tensor(selected_indices), torch.tensor(selected_values)

    def select(
        self,
        batch_size: int,
        model: M,
        dataset: Dataset,
        device: torch.device | None = None,
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        r"""
        Selects the next batch. If `force_nonsequential` is `True`, the data is selected analogously to `BatchAcquisitionFunction.select`.
        Otherwise, the data is selected by hierarchical composition of data selected from mini batches.

        :param batch_size: Size of the batch to be selected. Needs to be smaller than `mini_batch_size`.
        :param model: Model used for data selection.
        :param dataset: Inputs (shape $n \times d$) to be selected from.
        :param device: Device used for computation of the acquisition function.
        :return: Indices of the newly selected batch and corresponding values of the acquisition function.
        """
        if self.force_nonsequential:

            def compute_fn(
                model: M, data: torch.Tensor, device: torch.device | None = None
            ) -> torch.Tensor:
                return self.compute(self.initialize(model, data, device))

            return BatchAcquisitionFunction._select(
                compute_fn=compute_fn,
                batch_size=batch_size,
                model=model,
                dataset=dataset,
                device=device,
                mini_batch_size=self.mini_batch_size,
                num_workers=self.num_workers,
                subsample=self.subsample,
            )

        assert (
            batch_size < self.mini_batch_size
        ), "Batch size must be smaller than `mini_batch_size`."
        if batch_size > self.mini_batch_size / 2:
            warnings.warn(
                "The evaluation of the acquisition function may be slow since `batch_size` is large relative to `mini_batch_size`."
            )

        indexed_dataset = _IndexedDataset(dataset)
        selected_indices = None
        selected_values = None
        while (
            selected_indices is None or len(selected_indices) > batch_size
        ):  # gradually shrinks size of selected batch, until the correct size is reached
            data_loader = DataLoader(
                indexed_dataset,
                batch_size=self.mini_batch_size,
                num_workers=self.num_workers,
                shuffle=True,
            )

            selected_indices = []
            selected_values = []
            for data, idx in data_loader:
                sub_idx, sub_val = self.select_from_minibatch(
                    batch_size, model, data, device
                )
                selected_indices.extend(idx[sub_idx].cpu().tolist())
                selected_values.extend(sub_val.cpu().tolist())
                if self.subsample:
                    break
            indexed_dataset = Subset(indexed_dataset, selected_indices)
        return torch.tensor(selected_indices), torch.tensor(selected_values)


class EmbeddingBased(ABC):
    r"""
    Abstract base class for acquisition functions that require an embedding of the data.
    """

    embedding_batch_size: int = DEFAULT_EMBEDDING_BATCH_SIZE
    """Batch size used for computing the embeddings."""

    def __init__(
        self,
        embedding_batch_size=DEFAULT_EMBEDDING_BATCH_SIZE,
    ):
        """
        :param embedding_batch_size: Batch size used for computing the embeddings.
        """
        self.embedding_batch_size = embedding_batch_size

    @staticmethod
    def compute_embedding(
        model: ModelWithEmbedding | None,
        data: torch.Tensor,
        batch_size: int = DEFAULT_EMBEDDING_BATCH_SIZE,
    ) -> torch.Tensor:
        r"""
        Returns the embedding of the given data. If `model` is `None`, the data is returned as is (i.e., the data is assumed to be already embedded).

        :param model: Model used for computing the embedding.
        :param data: Tensor of inputs (shape $n \times d$) to be embedded.
        :param batch_size: Batch size used for computing the embeddings.
        :return: Embedding of the given data.
        """
        if model is None:
            return data

        device = get_device(model)
        model.eval()
        with torch.no_grad():
            embeddings = mini_batch_wrapper(
                fn=lambda batch: model.embed(
                    batch.to(device, non_blocking=True)
                ),  # TODO: handle device internally
                data=data,
                batch_size=batch_size,
            )
            return embeddings


class Targeted(ABC):
    r"""
    Abstract base class for acquisition functions that take into account the relevance of data with respect to a specified target (denoted $\spA$).
    """

    max_target_size: int | None
    r"""Maximum size of the target to be subsampled in each iteration."""

    subsampled_target_frac: float
    r"""Fraction of the target to be subsampled in each iteration. Must be in $(0,1]$."""

    def __init__(
        self,
        target: torch.Tensor,
        subsampled_target_frac: float = 1,
        max_target_size: int | None = None,
    ):
        r"""
        :param target: Tensor of prediction targets (shape $m \times d$).
        :param subsampled_target_frac: Fraction of the target to be subsampled in each iteration. Must be in $(0,1]$. Default is $1$.
        :param max_target_size: Maximum size of the target to be subsampled in each iteration. Default is `None` in which case the target may be arbitrarily large.
        """

        # assert target.size(0) > 0, "Target must be non-empty"
        assert (
            subsampled_target_frac > 0 and subsampled_target_frac <= 1
        ), "Fraction of target must be in (0, 1]"
        assert (
            max_target_size is None or max_target_size > 0
        ), "Max target size must be positive"

        self._target = target
        self.max_target_size = max_target_size
        self.subsampled_target_frac = subsampled_target_frac

    def add_to_target(self, new_target: torch.Tensor):
        r"""
        Appends new target data to the target.

        :param new_target: Tensor of new prediction targets (shape $m \times d$).
        """
        self._target = torch.cat([self._target, new_target])

    def set_target(self, new_target: torch.Tensor):
        r"""
        Updates the target.

        :param new_target: Tensor of new prediction targets (shape $m \times d$).
        """
        self._target = new_target

    def get_target(self) -> torch.Tensor:
        r"""
        Returns the tensor of (subsampled) prediction target (shape $m \times d$).
        """
        m = self._target.size(0)
        max_target_size = (
            self.max_target_size if self.max_target_size is not None else m
        )

        return self._target[
            torch.randperm(m)[
                : min(math.ceil(self.subsampled_target_frac * m), max_target_size)
            ]
        ]
