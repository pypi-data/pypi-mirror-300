from enum import Enum

from .passed import Passed
from .similarity_score import SimilarityScore


class MetricType(Enum):
    GROUNDEDNESS = "groundedness"
    CORRECTNESS = "correctness"
    PASSED = "passed"
    SIMILARITY_SCORE = "similarity_score"
    SCORE = "score"


    @staticmethod
    def get_class(metric_type):
        """
        Returns the class of the metric type.
        """
        if metric_type == MetricType.PASSED.value:
            return Passed
        elif metric_type == MetricType.SIMILARITY_SCORE.value:
            return SimilarityScore
        elif metric_type == MetricType.CORRECTNESS.value:
            return Passed
        elif metric_type == MetricType.CONVERSATION_RESOLUTION.value:
            raise NotImplementedError(
                f"Metric class is not implemented for {metric_type}"
            )
        else:
            raise NotImplementedError(f"Metric type {metric_type} not implemented.")
