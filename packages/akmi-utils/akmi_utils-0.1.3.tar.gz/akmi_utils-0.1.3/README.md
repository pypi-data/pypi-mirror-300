# akmi-utils

A utility package for converting TOML files to YAML format.

## Prerequisites

- Python 3.12 or higher
- Poetry

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/akmi-utils.git
    cd akmi-utils
    ```

2. Install dependencies using Poetry:
    ```sh
    poetry install
    ```

## Usage

To use the `convert_toml_to_yaml` function, follow these steps:

1. Import the function in your script:
    ```python
    from akmi_utils.convert_toml_yaml import convert_toml_to_yaml
    ```

2. Call the function with the input TOML file path and output YAML file path:
    ```python
    convert_toml_to_yaml('path/to/input.toml', 'path/to/output.yaml')
    ```

## Running Tests

To run the tests, use the following command:
```sh
poetry run pytest# utils