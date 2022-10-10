import abc


__all__ = ["Serializable"]


class Serializable(abc.ABC):
    @property
    @abc.abstractmethod
    def template_name(self) -> str:
        """The name of the template to use"""

    @abc.abstractmethod
    def to_xml(self) -> str:
        """Compiles object to Moodle XML"""
