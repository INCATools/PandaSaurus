Contributing & Development
==========================

Environment Setup
-----------------

1. Install Poetry (see https://python-poetry.org/docs/#installation).
2. Clone the repository and install dependencies:

   .. code-block:: bash

      poetry install

3. Activate the virtualenv:

   .. code-block:: bash

      poetry shell

Running Tests
-------------

Use pytest with coverage:

.. code-block:: bash

   poetry run pytest --cov=pandasaurus --cov-report=term-missing

Network-dependent tests hit Ubergraph. If you need deterministic runs, mock ``run_sparql_query`` as shown in ``test/test_query.py``.

Linting & Formatting
--------------------

Before committing, run:

.. code-block:: bash

   poetry run isort pandasaurus test
   poetry run black pandasaurus test
   poetry run flake8 pandasaurus test

The repository also includes a pre-commit hook (``.githooks/pre-commit``) that executes ``isort`` and ``black`` automatically if you configure ``core.hooksPath``.

Documentation
-------------

Docs live under ``docs/`` (Sphinx). Build them locally with:

.. code-block:: bash

   poetry install -E docs
   poetry run sphinx-build -b html docs docs/_build/html

CI publishes documentation from ``main`` to the ``gh-pages`` branch via GitHub Actions.

Release Pipeline
----------------

PyPI releases are automated: publishing a GitHub Release triggers the ``publish-pypi`` workflow, which builds the package via Poetry and uploads to PyPI using the ``PYPI_API_TOKEN`` secret.
