from . import Question

__all__ = ["MultiChoice"]


class MultiChoice(Question):
    @property
    def template_name(self) -> str:
        return "multichoice.xml"
