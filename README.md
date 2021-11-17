# Nautilus Filename Specification

## [💠 View Project Documentation 📖](https://nautilus-namecodes.readthedocs.io/en/latest/)

### (nautilus-namecodes)

*Nautilus namecodes are encoded filenames for media and other artistic creations in filesystem based content management systems.*

### Command Line Interface:

This application can be launched from the command line.

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


### Instructions

This repository uses [Poetry: Dependency Management for Python].

1. Install Python.

> [https://www.python.org/downloads/](https://www.python.org/downloads/)

2. Install Poetry.

> [https://github.com/python-poetry/poetry](https://github.com/python-poetry/poetry)

3. Clone the `nautilus-filename_specification` repository.

> [https://github.com/da2ce7/nautilus-filename_specification/tree/develop](https://github.com/da2ce7/nautilus-filename_specification/tree/develop)

4. Change Directory to the cloned repository:

> `cd nautilus-filename_specification`

5. Install Dependencies:

> `poetry install`

6. Run Tests:

> `poetry run tox`

7. Create Distribution Package:

> `poetry build`

[poetry: dependency management for python]: https://python-poetry.org/
