from collections.abc import Mapping
from typing import Any

from . import Question


__all__ = ["ShortAnswer"]


class ShortAnswer(Question):
    @property
    def template_name(self) -> str:
        return "shortanswer.xml"

    def question_data(self) -> Mapping[str, Any]:
        data = super().question_data()
        return data | {'case_sensitivity': int(data['case_sensitivity'])}
