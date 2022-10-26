from typing import Any, Mapping

from . import Question

__all__ = ["MultiChoice"]


class MultiChoice(Question):
    def _question_data(self) -> Mapping[str, Any]:
        return {}
