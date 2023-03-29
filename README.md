<p align="center">
    <a href="https://github.com/andrewthetechie/tf-vars-to-pydantic" target="_blank">
        <img src="https://img.shields.io/github/last-commit/andrewthetechie/tf-vars-to-pydantic" alt="Latest Commit">
    </a>
    <img src="https://img.shields.io/badge/license-MIT-green">
    <img alt="GitHub release (latest by date)" src="https://img.shields.io/github/v/release/andrewthetechie/tf-vars-to-pydantic?label=Latest%20Release">
    <br />
    <a href="https://github.com/andrewthetechie/tf-vars-to-pydantic/issues"><img src="https://img.shields.io/github/issues/andrewthetechie/tf-vars-to-pydantic" /></a>
    <img alt="GitHub Workflow Status Test and Lint (branch)" src="https://img.shields.io/github/actions/workflow/status/andrewthetechie/tf-vars-to-pydantic/tests.yml?branch=main">
    <img alt="Contributors" src="https://img.shields.io/github/contributors/andrewthetechie/tf-vars-to-pydantic">
    <br />
    <a href="https://pypi.org/project/tf-vars-to-pydantic" target="_blank">
        <img src="https://img.shields.io/pypi/v/tf-vars-to-pydantic" alt="Package version">
    </a>
    <img src="https://img.shields.io/pypi/pyversions/tf-vars-to-pydantic">
</p>

## Features

- Read a Terraform Variables HCL file (variables.tf) and create a Pydantic model from it
- Interpret complex data types (list(string), etc) into Python data types
- Interpret object data types into sub models
- Does not currently support terraform input validation

## Requirements

- Python ^3.11
- Pydantic ^1.10.x
- python-hcl2 ^4.3.x

## Installation

You can install _Tf Vars To Pydantic_ via [pip] from [PyPI]:

```console
pip install tf-vars-to-pydantic
```

## Usage

Assuming you have a tf vars file that looks like:

```
variable "foo" {
  description = "String variable"
  type        = string
}

variable "bar" {
  description = "String variable with default"
  type        = number
}

variable "baz" {
  type        = list(string)
}

variable "qux" {
  description = "Boolean variable"
  default     = true
  type        = bool
}
```

```python

from tf_vars_to_pydantic import convert_file

TFVarsModel = convert_file(path="./tests/fixtures/simple.tf", model_name="TFVarsModel")

tfvars_as_pydantic = TFVarsModel(foo="test", bar=7.2, baz=['boop', 'bing', 'bong'])
print(tfvars_as_pydantic)
# foo='test' bar=7.2 baz=['boop', 'bing', 'bong'] qux=True
```

## Contributing

Contributions are very welcome.
To learn more, see the [Contributor Guide].

## License

Distributed under the terms of the [MIT license][license],
_Tf Vars To Pydantic_ is free and open source software.

## Issues

If you encounter any problems,
please [file an issue] along with a detailed description.

<!-- github-only -->

[license]: https://github.com/andrewthetechie/tf-vars-to-pydantic/blob/main/LICENSE
[contributor guide]: https://github.com/andrewthetechie/tf-vars-to-pydantic/blob/main/CONTRIBUTING.md

## Contributors

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/andrewthetechie"><img src="https://avatars.githubusercontent.com/u/1377314?v=4?s=100" width="100px;" alt="Andrew"/><br /><sub><b>Andrew</b></sub></a><br /><a href="https://github.com/andrewthetechie/tf-vars-to-pydantic/commits?author=andrewthetechie" title="Code">💻</a> <a href="https://github.com/andrewthetechie/tf-vars-to-pydantic/commits?author=andrewthetechie" title="Tests">⚠️</a> <a href="https://github.com/andrewthetechie/tf-vars-to-pydantic/commits?author=andrewthetechie" title="Documentation">📖</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->
