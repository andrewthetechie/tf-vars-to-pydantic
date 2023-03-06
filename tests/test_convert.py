import hcl2
import pytest
from tf_vars_to_pydantic import convert
from tf_vars_to_pydantic import exceptions


def test_convert_file_valid(fixture_path):
    model = convert.convert_file(path=fixture_path / "valid.tf", model_name="TestModel")
    # read the fixture file in line by line and count all lines that start with variable
    with open(fixture_path / "valid.tf") as fh:
        lines = fh.readlines()
        num_vars = len([l for l in lines if l.startswith("variable")])

    assert len(model.__fields__) == num_vars
    assert model.__fields__["string_var"].type_ == str


def test_convert_file_not_variables(fixture_path):
    with pytest.raises(exceptions.HCLMissingVariablesError):
        convert.convert_file(path=fixture_path / "notvars.tf", model_name="Invalid")


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


def test_invalid_type_no_dollar_brace_raises_exception():
    with pytest.raises(exceptions.InvalidTFTypeStringError):
        convert._tf_type_to_python("blahblahblah")


def test_invaid_type_invalid_key_raises_exception():
    with pytest.raises(exceptions.InvalidTFTypeStringError):
        convert._tf_type_to_python("${blah}")


def test_invaid_type_invalid_outer_type_key_raises_exception():
    with pytest.raises(exceptions.InvalidTFTypeStringError):
        convert._tf_type_to_python("${blah(string)}")


def test_tf_object_with_defaults():
    data_str = "${object({'param1': '${string}'})}"
    defaults = {"param1": "test"}
    model = convert._tf_object_type_to_model(data_str, defaults)
    assert len(model.__fields__) == 1
    assert model.__fields__["param1"].default == "test"


def test_convert_default_type():
    data_str = """variable "string_var" {
                description = "String variable"
        }"""
    model = convert.convert_string(data_str=data_str, model_name="TestModel", default_type=str)
    assert len(model.__fields__) == 1
    assert model.__fields__["string_var"].type_ == str
