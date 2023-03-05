import hcl2
import pytest
from tf_vars_to_pydantic import convert
from tf_vars_to_pydantic import exceptions


def test_convert_file_valid():
    model = convert.convert_file(path="tests/fixtures/valid.tf", model_name="TestModel")

    assert model.__fields__["string_var"].type_ == str


def test_convert_file_not_variables():
    with pytest.raises(exceptions.HCLMissingVariablesError):
        convert.convert_file(path="tests/fixtures/notvars.tf", model_name="Invalid")


def test_convert_string():
    data_str = """variable "string_var" {
                    description = "String variable"
                    type        = string
            }"""
    model = convert.convert_string(data_str=data_str, model_name="TestModel")
    assert len(model.__fields__) == 1
    assert model.__fields__["string_var"].type_ == str


def test_convert_string_not_variables():
    data_str = """data "aws_caller_identity" "current" {}"""
    with pytest.raises(exceptions.HCLMissingVariablesError):
        convert.convert_string(data_str=data_str, model_name="TestModel")


def test_convert_missing_type_raises_exception(fixture_path):
    with open(fixture_path / "missing_type.tf") as fh:
        data = hcl2.load(fh)

    with pytest.raises(exceptions.VariableMissingTypeError):
        convert._convert(data, "TestModel", ignore_missing_types=False, default_type="none")
