# Pandasaurus

<img src="https://user-images.githubusercontent.com/112839/227489878-d253c381-75fd-4e92-b851-2b36df0fc5ed.png" width=100>

Pandasaurus supports simple queries over ontology annotations in dataframes, powered by Ubergraph SPARQL queries. It keeps dependencies light while still offering CURIE validation, enrichment utilities, and graph exports for downstream tooling.

## Features

- Validate and update seed CURIEs, catching obsoleted terms with replacement suggestions.
- Enrich seed lists via simple, minimal, full, contextual, and ancestor-based strategies.
- Build tabular outputs (`pandas.DataFrame`) and transitive-reduced graphs (`rdflib.Graph`) for visualization.
- Batched SPARQL queries and deterministic tests with built-in mocking examples.

## Installation

```bash
pip install pandasaurus
```

or with Poetry:

```bash
poetry add pandasaurus
```

Requires Python 3.9–3.11.

## Quick Example

```python
from pandasaurus.curie_validator import CurieValidator
from pandasaurus.query import Query

seeds = ["CL:0000084", "CL:0000787", "CL:0000636"]

terms = CurieValidator.construct_term_list(seeds)
CurieValidator.get_validation_report(terms)  # raises if invalid or obsoleted

query = Query(seeds, force_fail=True)
df = query.simple_enrichment()
print(df.head())
```

See the [Quick Start guide](docs/quickstart.rst) for a step-by-step workflow.

## Documentation

Full documentation (quick start, recipes, developer guide, and API reference) lives under `docs/` and is published from the `gh-pages` branch:

- [Quick Start](docs/quickstart.rst)
- [Guides](docs/guides/index.rst)
- [API reference](docs/pandasaurus/index.rst)

To build docs locally:

```bash
poetry install -E docs
poetry run sphinx-build -b html docs docs/_build/html
```

## Contributing

Pull requests are welcome! See `docs/guides/contributing.rst` for details on environment setup, testing, linting, and the release workflow. Pandasaurus aims to remain a small, focused library; please open an issue before introducing large new features.

## Background

The first planned use case is to provide enrichment/query tooling for AnnData Cell x Gene matrices following the [CZ single cell curation standard](https://github.com/chanzuckerberg/single-cell-curation/blob/main/schema/3.0.0/schema.md).
