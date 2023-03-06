from typing import Any
from typing import TypeVar

from pydantic import BaseModel

# objects are handled separately
TF_TYPE_MAP = {
    "string": str,
    "number": float,
    "bool": bool,
    "any": Any,
    "list": list,
    "map": dict,
    "set": set,
    "tuple": tuple,
}


Model = TypeVar("Model", bound="BaseModel")
