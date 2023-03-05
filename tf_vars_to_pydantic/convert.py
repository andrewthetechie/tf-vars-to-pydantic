import typing
from pathlib import Path
from typing import Any

import hcl2
from pydantic import BaseModel
from pydantic import create_model
from pydantic import Field

from .exceptions import HCLMissingVariablesError
from .exceptions import VariableMissingTypeError

Model = typing.TypeVar("Model", bound="BaseModel")


TERRAFORM_TYPE_TO_PYTHON_MAP = {
    "${string}": str,
    "${number}": float,
    "${bool}": bool,
    "${list(string)}": list[str],
    "${list(number)}": list[float],
    "${map(string)}": dict[str, str],
}


def convert_file(
    path: str | Path, model_name: str, ignore_missing_types: bool = True, default_type: str = "${string}"
) -> type[Model]:
    with open(path) as fh:
        data = hcl2.load(fh)
    if "variable" not in data:
        raise HCLMissingVariablesError(f"{path} is not a valid terraform module variables file")
    return _convert(
        data=data, model_name=model_name, ignore_missing_types=ignore_missing_types, default_type=default_type
    )


def convert_string(
    data_str: str | Path, model_name: str, ignore_missing_types: bool = True, default_type: str = "${string}"
) -> type[Model]:
    data = hcl2.loads(data_str)
    if "variable" not in data:
        raise HCLMissingVariablesError("String is not a valid terraform module variables file")
    return _convert(
        data=data,
        model_name=model_name,
        ignore_missing_types=ignore_missing_types,
        default_type=default_type,
    )


def _convert(data: dict[str, Any], model_name: str, ignore_missing_types: bool, default_type: str) -> type[Model]:
    field_definitions: Any = {}
    for variable in data["variable"]:
        variable_name = list(variable.keys())[0]
        variable = variable[variable_name]
        description = variable.get("description", "")
        var_type = variable.get("type", None)
        if var_type is None:
            if not ignore_missing_types:
                raise VariableMissingTypeError(f"{variable_name} is missing a type")
            else:
                var_type = default_type
        default = variable.get("default", None)
        if default is not None:
            this_field = Field(default, description=description)
        else:
            this_field = Field(..., description=description)
        field_definitions[variable_name] = (TERRAFORM_TYPE_TO_PYTHON_MAP[var_type], this_field)

    this_model: type[Model] = create_model(__model_name=model_name, **field_definitions)

    return this_model
