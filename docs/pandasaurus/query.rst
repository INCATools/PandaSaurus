Query
==================

Overview
--------

``Query`` orchestrates CURIE validation, enrichment, and graph generation on top of Ubergraph.

Typical workflow:

1. Construct with a seed list (list of CURIE strings).
2. Call an enrichment method (``simple_enrichment``, ``minimal_slim_enrichment``, ``contextual_slim_enrichment``, etc.).
3. Inspect the resulting DataFrame or export ``graph_df``/``graph``.

Key Attributes
--------------

* ``enriched_df`` – latest enrichment results as a pandas DataFrame.
* ``graph_df`` – edges suitable for plotting or exporting to external graph tooling.
* ``graph`` – rdflib graph with transitive reduction applied.

Class Reference
---------------

.. currentmodule:: pandasaurus.query

.. autoclass:: Query
   :members:
