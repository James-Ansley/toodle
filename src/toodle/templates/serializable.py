import abc

__all__ = ["Serializable"]


class Serializable(abc.ABC):
    @abc.abstractmethod
    def to_xml(self) -> str:
        """Compiles object to Moodle XML"""
