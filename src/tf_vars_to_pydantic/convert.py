import hcl2
from pydantic import BaseModel
from pydantic import create_model
from pydantic import Field

from .exceptions import HCLMissingVariablesError
from .exceptions import VariableMissingTypeError


TERRAFORM_TYPE_TO_PYTHON_MAP = {
    "${string}": str,
    "${number}": float,
    "${bool}": bool,
    "${list(string)}": list[str],
    "${list(number)}": list[float],
}


def file_to_pydantic_model(
    path: str, model_name: str, ignore_missing_types: bool = True, default_type: str = "${string}"
) -> BaseModel:
    with open(path) as fh:
        data = hcl2.load(fh)

    if "variable" not in data:
        raise HCLMissingVariablesError(f"{path} is not a valid terraform module variables file")

    model_args = {}
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
        model_args[variable_name] = (TERRAFORM_TYPE_TO_PYTHON_MAP[var_type], this_field)

    this_model = create_model(model_name, **model_args)

    return this_model
