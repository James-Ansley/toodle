import json
from collections.abc import Mapping
from pathlib import Path

from typing import Any

from jsonschema.validators import Draft7Validator


_ROOT = Path(__file__).parent
_SCHEMA_NAME_FORMAT = "{}-schema.json"


def get_schema(common_name: str) -> Mapping[str, Any]:
    path = _ROOT / _SCHEMA_NAME_FORMAT.format(common_name)
    with open(path) as f:
        return json.load(f)


def validate(common_name: str, config: Mapping[str, Any]):
    schema = get_schema(common_name)
    validator = Draft7Validator(schema)
    res = validator.is_valid(config)
    print(*validator.iter_errors(config), sep="\n")
    return res
