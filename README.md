# gusto

Ever wanted to find the word count for a PDF file but don't trust a dodgy website with your documents?!?! gusto is the tool for you !!

gusto is a file and metadata analysis tool designed to extract information from files of all different types !!

This is **groundbreaking!!!** Not even the inventors of the PDF format (Adobe) know how to count the words in a PDF !!


## Installation

1. Clone this repo or download the zip.
2. Open terminal and use `cd /path/to/directory` to navigate to the project folder (the one that has the `pyproject.toml` file)
3. Then use of these to install it:

    ```bash
    pip install .
    ```

    Or install with `pipx` for an isolated CLI tool:

    ```bash
    pipx install .
    ```

4. Finally, use `gusto <file>` to analyse your file :D


## Usage

### Analyse a file

```bash
gusto <file>
```

Example:

```bash
gusto trying_my_best.pdf
```


### Analyse all files in a folder

```bash
gusto <directory>
```

Example:

```bash
gusto ~/Documents/projects
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

