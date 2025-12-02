Overview
========

Pandasaurus supports simple queries over ontology annotations in dataframes, powered by Ubergraph SPARQL queries. It keeps dependencies light while still offering CURIE validation, enrichment utilities, and graph exports for downstream tooling.

Features
--------

- Validate and update seed CURIEs, catching obsoleted terms with replacement suggestions.
- Enrich seed lists via simple, minimal, full, contextual, and ancestor-based strategies.
- Build tabular outputs (:class:`pandas.DataFrame`) and transitive-reduced graphs (:class:`rdflib.Graph`) for visualization.
- Batched SPARQL queries and deterministic tests with built-in mocking examples.

Installation
------------

.. code-block:: bash

   pip install pandasaurus

or with Poetry:

.. code-block:: bash

   poetry add pandasaurus

Requires Python 3.9–3.11.

Quick Example
-------------

.. code-block:: python

   from pandasaurus.curie_validator import CurieValidator
   from pandasaurus.query import Query

   seeds = ["CL:0000084", "CL:0000787", "CL:0000636"]

   terms = CurieValidator.construct_term_list(seeds)
   CurieValidator.get_validation_report(terms)  # raises if invalid or obsoleted

   query = Query(seeds, force_fail=True)
   df = query.simple_enrichment()
   print(df.head())

Continue to :doc:`quickstart` for a full workflow.

.. seealso::
   Jump straight into the detailed walkthrough in :doc:`quickstart`.

Documentation Links
-------------------

- :doc:`quickstart`
- :doc:`guides/index`
- :doc:`pandasaurus/index`

Background
----------

The first planned use case is to provide enrichment/query tooling for AnnData Cell x Gene matrices following the `CZ single cell curation standard <https://github.com/chanzuckerberg/single-cell-curation/blob/main/schema/3.0.0/schema.md>`_.
