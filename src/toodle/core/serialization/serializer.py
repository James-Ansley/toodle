import abc
from collections.abc import Iterable

from toodle.core.serialization import Serializable


class Serializer(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def serialize(cls, target: Serializable) -> str:
        """Serializes the target to a string"""

    @classmethod
    @abc.abstractmethod
    def serialize_all(cls, target: Iterable[Serializable]) -> str:
        """Serializes the target and children to a string"""
