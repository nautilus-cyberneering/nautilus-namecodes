# Nautilus Filename Specification

## [💠 View Project Documentation 📖](https://nautilus-namecodes.readthedocs.io/en/latest/)

## [💠 View Project on the Python Package Index 📦](https://pypi.org/project/nautilus-namecodes/)

### (nautilus-namecodes)

*Nautilus namecodes are encoded filenames for media and other artistic creations in filesystem based content management systems.*

### Installation

To instal this application you can use pip: [package installer for Python](https://pip.pypa.io/en/latest/).

`pip3 install nautilus-namecodes`

### Command Line Interface:

While this application is primarily focused as an application library, a small command line interface is included.

For example you can print all the Name Codes with this command:

`nautilus-namecodes codes --show-all`

### Libraries Used

* This project depends on 'atoml' for processing the pyproject.toml file.
  
  MIT License Copyright (c) 2021 Frost Ming, 2018 Sébastien Eustace

  > [https://github.com/frostming/atoml](https://github.com/frostming/atoml)

* This project depends on 'typer' for creating the CLI.

  MIT License Copyright (c) 2019 Sebastián Ramírez

  > [https://github.com/tiangolo/typer](https://github.com/tiangolo/typer)

### Notes

* This repository uses "pytest" to run python tests code.

> [https://docs.pytest.org/en/latest/](https://docs.pytest.org/en/latest/)

* This repository uses "Black" to format python code.

> [https://black.readthedocs.io/en/latest/](https://black.readthedocs.io/en/latest/)

* This repository uses "mypy" to type check the python code.

> [https://github.com/python/mypy](https://github.com/python/mypy)

* This repository uses 'pylint' to check the python code quality.

> [https://pylint.org/](https://pylint.org/)

* This repository uses 'bandit' to code for security issues.

> [https://bandit.readthedocs.io/en/latest/](https://bandit.readthedocs.io/en/latest/)

* This repository uses 'isort' to check that imports are sorted.

> [https://pycqa.github.io/isort/](https://pycqa.github.io/isort/)

* This repository uses Sphinx and Myst-Parser for documentation infrastructure.

> [https://www.sphinx-doc.org/en/master/](https://www.sphinx-doc.org/en/master/)
> [https://github.com/executablebooks/MyST-Parser](https://github.com/executablebooks/MyST-Parser)


### Development Instructions

This repository uses [Poetry: Dependency Management for Python, include the 'Poetry Dynamic Versioning' extension].

1. Install Python.

> [https://www.python.org/downloads/](https://www.python.org/downloads/)
s
2. Install Poetry and Poetry Dynamic Versioning

> `pip3 install poetry poetry-dynamic-versioning`

3. Clone the `nautilus-namecodes` repository development tree.

> [https://github.com/da2ce7/nautilus-namecodes/tree/develop](https://github.com/da2ce7/nautilus-namecodes/tree/develop)

4. Change Directory to the cloned repository:

> `cd nautilus-filename_specification`

5. Install Dependencies:

> `poetry install`

6. Run Tests:

> `poetry run tox`

7. Create Distribution Package:

> `poetry build`

[poetry: dependency management for python]: https://python-poetry.org/
