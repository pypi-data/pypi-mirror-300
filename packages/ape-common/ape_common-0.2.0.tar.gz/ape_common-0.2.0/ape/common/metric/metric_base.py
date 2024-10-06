from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Union
import asyncio

from ape.common.types import MetricResult, DatasetItem


class BaseMetric(ABC):
    @abstractmethod
    async def compute(
        self,
        dataset_item: DatasetItem,
        pred: Union[str, Dict[str, Any]]
    ) -> MetricResult:
        """
        Compute the metric. This method can be implemented as either synchronous or asynchronous.

        Args:
            dataset_item (DatasetItem): The dataset item to evaluate. it includes inputs, outputs, and metadata as attributes.
            pred (Union[str, Dict[str, Any]]): The prediction to evaluate.

        Returns:
            MetricResult: An object containing the computed score and any intermediate values.

        Note:
            The implementation of this method should handle the comparison between `pred` and `dataset_item["outputs"]`,
            potentially using the information in `dataset_item["inputs"]` and `dataset_item["metadata"]` to inform the computation.
            It should return a MetricResult object that encapsulates the result of the metric calculation.
        """
        pass

    async def __call__(
        self,
        *,
        dataset_item: DatasetItem,
        pred: Union[str, Dict[str, Any]]
    ) -> MetricResult:
        """
        Unified method to compute the metric, handling both sync and async implementations.

        Args:
            dataset_item (DatasetItem): The dataset item to evaluate.
            pred (Union[str, Dict[str, Any]]): The prediction.

        Returns:
            MetricResult: An object containing the score and intermediate values.
        """
        result = self.compute(dataset_item=dataset_item, pred=pred)
        if asyncio.iscoroutine(result):
            return await result
        return result
