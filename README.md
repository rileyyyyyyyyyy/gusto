# gusto

gusto is a file and metadata analysis tool designed to extract information from files of different types.


## Installation

```bash
pip install .
```

Or install with `pipx` for an isolated CLI tool:

```bash
pipx install .
```


## Usage

Run the CLI by invoking the script:

```bash
gusto <file_path>
```

Example:

```bash
gusto example.pdf
```


## Project Structure

```
gusto/
├── __init__.py
├── __main__.py        # CLI entry point
├── adapter.py         # File adapter classes for typing
├── analysis.py        # Analysis logic
pyproject.toml         # Build and dependency specification
```

