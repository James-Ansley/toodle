import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any, Type

from jsonschema.validators import RefResolver, validate as _validate

_SCHEMATA_ROOT = (Path(__file__) / ".." / "schemata").resolve()


def validate(target_type: Type, data: Mapping[str, Any]):
    """
    Validates a heterogeneous string map of object data against the json
    schema for that object's type

    :param target_type: The type of object
    :param data: The heterogeneous string map of public object data

    :raises jsonschema.exceptions.ValidationError: If the data does not
        satisfy the json schema
    """
    schema_path = _SCHEMATA_ROOT / f"{target_type.__name__.lower()}.schema.json"
    with open(schema_path, "r") as f:
        schema = json.load(f)
    resolver = RefResolver(f"{_SCHEMATA_ROOT.as_uri()}/", True)
    _validate(data, schema, resolver=resolver)
