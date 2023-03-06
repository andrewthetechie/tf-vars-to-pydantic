from ast import literal_eval
from pathlib import Path
from typing import Any
from typing import TypeVar

import hcl2
from pydantic import create_model
from pydantic import Field

from . import _typing
from .exceptions import HCLMissingVariablesError
from .exceptions import InvalidTFTypeStringError
from .exceptions import VariableMissingTypeError


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
) -> type[_typing.Model]:
    with open(path) as fh:
        data = hcl2.load(fh)
    if "variable" not in data:
        raise HCLMissingVariablesError(f"{path} is not a valid terraform module variables file")
    return _convert(
        data=data, model_name=model_name, ignore_missing_types=ignore_missing_types, default_type=default_type
    )


def convert_string(
    data_str: str | Path, model_name: str, ignore_missing_types: bool = True, default_type: str = "${string}"
) -> type[_typing.Model]:
    data = hcl2.loads(data_str)
    if "variable" not in data:
        raise HCLMissingVariablesError("String is not a valid terraform module variables file")
    return _convert(
        data=data,
        model_name=model_name,
        ignore_missing_types=ignore_missing_types,
        default_type=default_type,
    )


def _convert(
    data: dict[str, Any], model_name: str, ignore_missing_types: bool, default_type: str
) -> type[_typing.Model]:
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
        else:
            var_type = _tf_type_to_python(var_type)
        default = variable.get("default", None)
        if default is not None:
            this_field = Field(default, description=description)
        else:
            this_field = Field(..., description=description)
        field_definitions[variable_name] = (var_type, this_field)

    this_model: type[_typing.Model] = create_model(__model_name=model_name, **field_definitions)

    return this_model


def _tf_type_to_python(tf_type_str: str, default: Any = None) -> TypeVar:
    """Convert a terraform type string from the hcl2 loaded data into a python typing.

    Will step through the string to solve for complex types"""
    if not tf_type_str.startswith("${") and not tf_type_str.endswith("}"):
        raise InvalidTFTypeStringError(f"{tf_type_str} is not a valid type string")

    # find the index of the first ( and use it to find our base type
    if (opening_index := tf_type_str.find("(")) == -1:
        # no ( means this is not a complex type
        try:
            return _typing.TF_TYPE_MAP[(type_as_string := tf_type_str[2:].strip(")")[:-1])]
        except KeyError as exc:
            # an object with no further description can just be treated like a map with no specification
            # so a dict
            if type_as_string == "object":
                return _typing.TF_TYPE_MAP["map"]
            raise InvalidTFTypeStringError(f"{tf_type_str} is not a valid type string") from exc

    outer_type_str = tf_type_str[:opening_index][2:]

    if outer_type_str == "object":
        return _tf_object_type_to_model(tf_type_str, defaults={} if default is None else default)
    try:
        # get the string of the outermost type and strip out the ${
        outer_type = _typing.TF_TYPE_MAP[tf_type_str[:opening_index][2:]]
    except KeyError as exc:
        raise InvalidTFTypeStringError(
            f"{tf_type_str} is not a valid terraform type string."
            + f"{tf_type_str[:opening_index][2:]} is not in the type map"
        ) from exc

    # recurse, stripping out the outer type we've already handled
    inner_type_str = f"${{{tf_type_str[opening_index + 1:-2]}}}"
    if outer_type == dict:
        return outer_type[str, _tf_type_to_python(inner_type_str)]
    return outer_type[_tf_type_to_python(inner_type_str)]


def _tf_object_type_to_model(tf_object_str: str, defaults: dict[str, Any] = {}) -> type[_typing.Model]:
    """Convert a hcl2 str for a terraform object into a pydantic model"""
    # strip the outer ${} and the object fields are a valid dict[str, str]
    field_definitions = {}
    for field_name, type_string in literal_eval(tf_object_str[: tf_object_str.find("'}") + 2][9:]).items():
        if field_name in defaults:
            this_field = Field(defaults[field_name])
        else:
            this_field = Field(...)
        field_definitions[field_name] = (_tf_type_to_python(type_string), this_field)
    return create_model(__model_name="TFObject", **field_definitions)
