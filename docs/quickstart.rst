Quick Start
===========

This page walks through the most common workflow: validating a list of CURIEs, enriching them, and inspecting the results.

.. seealso::
   For a high-level summary, read :doc:`overview`.

Installation
------------

Pandasaurus requires Python 3.9–3.11. Install with pip or Poetry:

.. code-block:: bash

   pip install pandasaurus

or

.. code-block:: bash

   poetry add pandasaurus

Validate CURIEs
---------------

Use :class:`pandasaurus.curie_validator.CurieValidator` to confirm that your seed terms exist and aren't obsoleted:

.. code-block:: python

   from pandasaurus.curie_validator import CurieValidator

   seeds = ["CL:0000084", "CL:0000787", "CL:0000636"]
   terms = CurieValidator.construct_term_list(seeds)
   CurieValidator.get_validation_report(terms)  # raises if invalid or obsoleted

Handle Invalid Terms
~~~~~~~~~~~~~~~~~~~~

If :class:`pandasaurus.utils.pandasaurus_exceptions.InvalidTerm` is raised, inspect the invalid IRIs from the exception message, update your seed list, and rerun.

Run an Enrichment
-----------------

Instantiate :class:`pandasaurus.query.Query` with your validated CURIEs and call an enrichment method, e.g. :meth:`~pandasaurus.query.Query.simple_enrichment`:

.. code-block:: python

   from pandasaurus.query import Query

   query = Query(seeds, force_fail=True)
   df = query.simple_enrichment()
   print(df.head())

`force_fail=True` ensures the constructor raises immediately on invalid or obsoleted terms.

Review Obsoleted Terms
----------------------

If the seed list contains obsoleted CURIEs, use :meth:`~pandasaurus.query.Query.update_obsoleted_terms` to replace them with their suggested alternatives:

.. code-block:: python

   query.update_obsoleted_terms()

Generate a Graph
----------------

Every enrichment populates :attr:`pandasaurus.query.Query.graph_df`, which can be converted into a NetworkX-compatible graph:

.. code-block:: python

   graph = query.graph  # rdflib.Graph after transitive reduction
   # or export query.graph_df for plotting

Next Steps
----------

* Explore advanced methods (``minimal_slim_enrichment``, ``contextual_slim_enrichment``) in the :doc:`Query API <pandasaurus/query>`.
* See :doc:`guides/index` for task-focused recipes.
* Visit :doc:`guides/contributing` to learn how to run tests, linting, and documentation builds locally.
