# RosettaFinder

A Python utility for finding Rosetta binaries based on a specific naming convention.

![GitHub License](https://img.shields.io/github/license/YaoYinYing/RosettaPy)


## CI Status
[![Python CI](https://github.com/YaoYinYing/RosettaPy/actions/workflows/CI.yml/badge.svg)](https://github.com/YaoYinYing/RosettaPy/actions/workflows/CI.yml)
[![Dependabot Updates](https://github.com/YaoYinYing/RosettaPy/actions/workflows/dependabot/dependabot-updates/badge.svg)](https://github.com/YaoYinYing/RosettaPy/actions/workflows/dependabot/dependabot-updates)
[![codecov](https://codecov.io/gh/YaoYinYing/RosettaPy/branch/main/graph/badge.svg?token=epCTnx8SXj)](https://codecov.io/gh/YaoYinYing/RosettaPy)

## Release
![GitHub Release](https://img.shields.io/github/v/release/YaoYinYing/RosettaPy)
![GitHub Release Date](https://img.shields.io/github/release-date/YaoYinYing/RosettaPy)

![PyPI - Format](https://img.shields.io/pypi/format/RosettaPy)
![PyPI - Version](https://img.shields.io/pypi/v/RosettaPy)
![PyPI - Status](https://img.shields.io/pypi/status/RosettaPy)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/RosettaPy)


## Python version supported
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/RosettaPy)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/RosettaPy)




## Overview

`RosettaFinder` is a Python module designed to locate Rosetta biomolecular modeling suite binaries that follow a specific naming pattern. It searches predefined directories and can handle custom search paths. The module includes:

- An object-oriented `RosettaFinder` class to search for binaries.
- A `RosettaBinary` dataclass to represent the binary and its attributes.
- A command-line shortcut for quick access to Rosetta binaries.
- Unit tests to ensure reliability and correctness.

## Features

- **Flexible Binary Search**: Finds Rosetta binaries based on their naming convention.
- **Platform Support**: Supports Linux and macOS operating systems.
- **Customizable Search Paths**: Allows specification of custom directories to search.
- **Structured Binary Representation**: Uses a dataclass to encapsulate binary attributes.
- **Command-Line Shortcut**: Provides a quick way to find binaries via the command line.
- **Available on PyPI**: Installable via `pip` without the need to clone the repository.
- **Unit Tested**: Includes tests for both classes to ensure functionality.

## Naming Convention

The binaries are expected to follow this naming pattern:

```
rosetta_scripts[.mode].oscompilerrelease
```

- **Binary Name**: `rosetta_scripts` (default) or specified.
- **Mode** (optional): `default`, `mpi`, or `static`.
- **OS**: `linux` or `macos`.
- **Compiler**: `gcc` or `clang`.
- **Release**: `release` or `debug`.

Examples of valid binary filenames:

- `rosetta_scripts.linuxgccrelease`
- `rosetta_scripts.mpi.macosclangdebug`
- `rosetta_scripts.static.linuxgccrelease`

## Installation

Ensure you have Python 3.6 or higher installed.

### Install via PyPI

You can install `RosettaPy` directly from PyPI:

```bash
pip install RosettaPy -U
```

This allows you to use `RosettaPy` without cloning the repository.

## Usage

### Command-Line Shortcut

`RosettaPy` provides a command-line shortcut to quickly locate Rosetta binaries.

#### Using the `whichrosetta` Command

After installing `RosettaPy`, you can use the `whichrosetta` command in your terminal.

```bash
whichrosetta <binary_name>
```

**Example:**

To find the `relax` binary:

```bash
relax_bin=$(whichrosetta relax)
echo $relax_bin
```

This command assigns the full path of the `relax` binary to the `relax_bin` variable and prints it.

### Importing the Module

You can also use `RosettaPy` in your Python scripts.

```python
from RosettaPy import RosettaFinder, RosettaBinary
```

### Finding a Rosetta Binary in Python

```python
# Initialize the finder (optional custom search path)
finder = RosettaFinder(search_path='/custom/path/to/rosetta/bin')

# Find the binary (default is 'rosetta_scripts')
rosetta_binary = finder.find_binary('rosetta_scripts')

# Access binary attributes
print(f"Binary Name: {rosetta_binary.binary_name}")
print(f"Mode: {rosetta_binary.mode}")
print(f"OS: {rosetta_binary.os}")
print(f"Compiler: {rosetta_binary.compiler}")
print(f"Release: {rosetta_binary.release}")
print(f"Full Path: {rosetta_binary.full_path}")
```

### Example Output

```
Binary Name: rosetta_scripts
Mode: mpi
OS: linux
Compiler: gcc
Release: release
Full Path: /custom/path/to/rosetta/bin/rosetta_scripts.mpi.linuxgccrelease
```

## Environment Variables

The `RosettaFinder` searches the following directories by default:

1. The path specified in the `ROSETTA_BIN` environment variable.
2. `ROSETTA3/bin`
3. `ROSETTA/main/source/bin/`
4. A custom search path provided during initialization.

Set the `ROSETTA_BIN` environment variable to include your custom binary directory:

```bash
export ROSETTA_BIN=/path/to/your/rosetta/bin
```

## API Reference

### `whichrosetta` Command

The `whichrosetta` command is installed as part of the `RosettaPy` package and allows you to find the path to a Rosetta binary from the command line.

**Usage:**

```bash
whichrosetta <binary_name>
```

- `binary_name`: The name of the Rosetta binary you want to locate (e.g., `relax`, `rosetta_scripts`).

**Example:**

```bash
relax_bin=$(whichrosetta relax)
echo $relax_bin
```

This command finds the `relax` binary and prints its full path.

### `RosettaFinder` Class

- **Initialization**

  ```python
  RosettaFinder(search_path=None)
  ```

  - `search_path` (optional): A custom directory to include in the search paths.

- **Methods**

  - `find_binary(binary_name='rosetta_scripts')`

    Searches for the specified binary and returns a `RosettaBinary` instance.

    - `binary_name` (optional): Name of the binary to search for.

    - **Raises**:
      - `FileNotFoundError`: If the binary is not found.
      - `EnvironmentError`: If the OS is not Linux or macOS.

### `RosettaBinary` Dataclass

- **Attributes**

  - `dirname`: Directory where the binary is located.
  - `binary_name`: Base name of the binary.
  - `mode`: Build mode (`static`, `mpi`, `default`, or `None`).
  - `os`: Operating system (`linux` or `macos`).
  - `compiler`: Compiler used (`gcc` or `clang`).
  - `release`: Build type (`release` or `debug`).

- **Properties**

  - `filename`: Reconstructed filename based on the attributes.
  - `full_path`: Full path to the binary executable.

- **Class Methods**

  - `from_filename(dirname: str, filename: str)`

    Creates an instance by parsing the filename.

    - **Raises**:
      - `ValueError`: If the filename does not match the expected pattern.

## Running Tests

The project includes unit tests using Python's `unittest` framework.

### Running Tests

1. Clone the repository (if not already done):

   ```bash
   git clone https://github.com/yourusername/RosettaPy.git
   cd RosettaPy
   ```

2. Navigate to the project directory:

   ```bash
   cd RosettaPy
   ```

3. Run the tests:

   ```bash
   python -m unittest discover tests
   ```

### Test Coverage

The tests cover:

- Parsing valid and invalid filenames with `RosettaBinary`.
- Finding binaries with `RosettaFinder`, including scenarios where binaries are found or not found.
- OS compatibility checks.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for bug reports and feature requests.

## License

This project is licensed under the MIT License.

## Acknowledgements

- **Rosetta Commons**: The Rosetta software suite for the computational modeling and analysis of protein structures.

## Contact

For questions or support, please contact:

- **Name**: Yinying Yao
- **Email**:yaoyy.hi(a)gmail.com
