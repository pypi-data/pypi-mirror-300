import torch
import heapq
from typing import List, Tuple
from activeft.model import Model

Element = Tuple[int, float]
"""`(index, value)`"""

DEFAULT_MINI_BATCH_SIZE = 1_000
DEFAULT_EMBEDDING_BATCH_SIZE = 100
DEFAULT_NUM_WORKERS = 0
DEFAULT_SUBSAMPLE = False


def get_device(model: Model):
    return next(model.parameters()).device


def mini_batch_wrapper_non_cat(fn, data, batch_size):
    n_batches = int(data.size(0) / batch_size)
    results = []
    for i in range(n_batches + 1):
        mini_batch = data[i * batch_size : (i + 1) * batch_size]
        if len(mini_batch) == 0:
            continue
        result = fn(mini_batch)
        results.append(result)
    return results


def mini_batch_wrapper(fn, data, batch_size):
    results = mini_batch_wrapper_non_cat(fn, data, batch_size)
    return torch.cat(results, dim=0)


def wandb_log(data):
    try:
        import wandb

        if wandb.run is not None:
            wandb.log(data)
    except ImportError:
        # wandb is not installed; do nothing
        pass


class PriorityQueue(object):
    """Priority Queue (largest value first)"""

    def __init__(self, values: List[float]):
        """
        Initializes the priority queue.
        """
        self.q = [(-value, idx) for idx, value in enumerate(values)]
        heapq.heapify(self.q)

    @property
    def top(self) -> Element:
        """Returns the top element with the maximum value"""
        value, idx = self.q[0]
        return idx, -value

    @property
    def top_value(self) -> float:
        """Returns the maximum value"""
        return self.top[1]

    def pop(self) -> Element:
        """Pops and returns the top element with the maximum value"""
        value, idx = heapq.heappop(self.q)
        return idx, -value

    def push(self, idx: int, value: float):
        """Pushes to the priority queue"""
        heapq.heappush(self.q, (-value, idx))

    def size(self) -> int:
        """Returns the size of the priority queue"""
        return len(self.q)

    def empty(self):
        """Checks if the priority queue is empty"""
        return self.size() == 0
