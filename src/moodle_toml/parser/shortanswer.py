from functools import cached_property
from typing import Any

from .question import Question

__all__ = ["ShortAnswer"]


class ShortAnswer(Question):
    _XML_NAME = "shortanswer.xml"

    @cached_property
    def config(self) -> dict[str, Any]:
        config = super().config
        config['case_sensitivity'] = int(config['case_sensitivity'])
        return config
