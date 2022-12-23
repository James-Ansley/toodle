import abc
from typing import Any, Mapping

from toodle.core.serialization.schema_validation import validate


class Serializable(abc.ABC):
    def serialize(self):
        """
        Returns a heterogeneous string map of public type data.
        Validates the type against its corresponding json schema and type
        specific validation.
        """
        data = self._serialize()
        self.__validate(data)
        return data

    def validate(self):
        """
        Validates the type against its corresponding json schema and type
        specific validation.
        """
        data = self._serialize()
        validate(type(self), data)
        self._validate()

    def __validate(self, data):
        validate(type(self), data)
        self._validate()

    @abc.abstractmethod
    def _serialize(self) -> Mapping[str, Any]:
        """
        Provides a heterogeneous string map of the object data with no
        validation.
        """

    @abc.abstractmethod
    def _validate(self):
        """Validates question type specific dynamic requirements"""
