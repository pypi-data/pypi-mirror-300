from __future__ import annotations
from dataclasses import dataclass, field
from typing import Union
import torch
import torch.nn.functional as F
from typing import Any


def cosine_similarity(tensor1: torch.Tensor, tensor2: torch.Tensor) -> torch.Tensor:
    """
    Computes the cosine similarity between two tensors.

    :param tensor1: First input tensor of any shape
    :param tensor2: Second input tensor of the same shape as tensor1
    :returns: Cosine similarity value(s) as a tensor
    """
    tensor1_flat = tensor1.reshape(tensor1.size(0), -1)  # Flatten the tensor
    tensor2_flat = tensor2.reshape(tensor2.size(0), -1)  # Flatten the tensor

    # Compute the cosine similarity
    similarity = F.cosine_similarity(tensor1_flat, tensor2_flat, dim=1).item()

    return similarity


class SimilarityCollection:
    def __init__(self, query: Union[torch.Tensor, tuple[torch.Tensor, Any]], tensors: list[Union[torch.Tensor, tuple[torch.Tensor, Any]]]) -> None:
        """
        Initializes the SimilarityCollection with a query and a list of tensors or tuples containing tensors.

        :param query: The query tensor or tuple containing a tensor.
        :param tensors: A list of tensors or tuples containing tensors.
        """
        self.entries: list[SimilarityCollection.SimilarityCollectionItem] = []
        self.query = query
        try:
            for data in tensors:
                self._add(0, data)
        except SimilarityCollection.SimilarityCollectionItemError as e:
            raise SimilarityCollection.SimilarityCollectionItemError(
                "All items in the tensors list must be a tensor, or must be a list or tuple where the first item is a tensor"
            ) from e

    def _add(self, similarity: float, value: Union[torch.Tensor, tuple[torch.Tensor, Any]]) -> SimilarityCollection.SimilarityCollectionItem:
        """
        Adds a new item to the collection with a similarity score.

        :param similarity: Cosine similarity score between query and value
        :param value: The tensor or tuple containing a tensor
        :returns: The newly added SimilarityCollectionItem
        """
        entry = SimilarityCollection.SimilarityCollectionItem(
            similarity, value)
        self.entries.append(entry)
        return entry

    def __str__(self) -> str:
        string = "[\n"

        len_entries = len(self.entries)
        for i, entry in enumerate(self.entries):
            string += f"    ({round(entry.similarity, 4)
                             :.4f}, {type(entry.value).__name__})"
            if i < len_entries - 1:
                string += ", \n"
        string += "\n]"
        return string

    def _get_tensor(self, value: Union[torch.Tensor, tuple[torch.Tensor, Any]]) -> torch.Tensor | None:
        """
        Extracts the tensor from a value. Handles both tensors and tuples/lists containing tensors.

        :param value: A tensor or tuple/list containing a tensor as the first element
        :returns: The tensor if found, otherwise None
        """
        if isinstance(value, torch.Tensor):
            return value
        elif isinstance(value, (tuple, list)) and isinstance(value[0], torch.Tensor):
            return value[0]
        return None

    def sort(self) -> list[SimilarityCollection.SimilarityCollectionItem]:
        """
        Sorts the entries based on cosine similarity to the query and returns the sorted list.

        :returns: The sorted list of SimilarityCollectionItem with highest similarity first.
        """
        query_tensor = self._get_tensor(self.query)
        if query_tensor is None:
            raise ValueError("Query must be or contain a tensor")

        # Calculate cosine similarity for each entry
        for entry in self.entries:
            tensor = self._get_tensor(entry.value)
            if tensor is not None:
                similarity = cosine_similarity(
                    query_tensor, tensor)
                entry.similarity = similarity  # Update the similarity score

        # Sort the entries by similarity in descending order
        self.entries.sort(key=lambda x: x.similarity, reverse=True)

        return self.entries

    def low(self, threshold: float) -> SimilarityCollection.SimilarityCollectionItemGroup:
        sample = []
        for item in self.entries:
            if item.similarity <= threshold:
                sample.append(item)

        return SimilarityCollection.SimilarityCollectionItemGroup(sample)

    def high(self, threshold: float) -> SimilarityCollection.SimilarityCollectionItemGroup:
        sample = []
        for item in self.entries:
            if item.similarity >= threshold:
                sample.append(item)

        return SimilarityCollection.SimilarityCollectionItemGroup(sample)

    def range(self, min: float, max: float) -> SimilarityCollection.SimilarityCollectionItemGroup:
        sample = []
        for item in self.entries:
            if item.similarity >= min and item.similarity <= max:
                sample.append(item)

        return SimilarityCollection.SimilarityCollectionItemGroup(sample)

    @dataclass
    class SimilarityCollectionItem:
        similarity: float = 0
        value: Union[torch.Tensor, tuple[torch.Tensor, Any]] = None

    @dataclass
    class SimilarityCollectionItemGroup:
        items: list[SimilarityCollection.SimilarityCollectionItem] = field(
            default_factory=list)

        def __str__(self) -> str:
            string = "[\n"

            len_entries = len(self.items)
            for i, entry in enumerate(self.items):
                string += f"    ({round(entry.similarity, 4)
                                 :.4f}, {type(entry.value).__name__})"
                if i < len_entries - 1:
                    string += ", \n"
            string += "\n]"
            return string

    class SimilarityCollectionItemError(ValueError):
        def __init__(self, *args: object) -> None:
            super().__init__(*args)
