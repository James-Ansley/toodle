from collections.abc import Mapping
from typing import Any

from . import Question


__all__ = ["ShortAnswer"]


class ShortAnswer(Question):
    def _question_data(self) -> Mapping[str, Any]:
        return {'casesensitivity': int(self.config()['casesensitivity'])}
