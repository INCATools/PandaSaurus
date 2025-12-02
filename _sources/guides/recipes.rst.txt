Task-Oriented Recipes
=====================

Validate and Update Seeds
-------------------------

1. Construct the term list:

   .. code-block:: python

      from pandasaurus.curie_validator import CurieValidator

      terms = CurieValidator.construct_term_list(seeds)

2. Catch validation errors:

   .. code-block:: python

      from pandasaurus.utils.pandasaurus_exceptions import InvalidTerm, ObsoletedTerm

      try:
          CurieValidator.get_validation_report(terms)
      except InvalidTerm as err:
          print(err)
      except ObsoletedTerm as err:
          print(err)

3. Replace obsoleted terms programmatically:

   .. code-block:: python

      query = Query(seeds)
      query.update_obsoleted_terms()

Contextual Enrichment
---------------------

Gather all terms that are ``part_of`` a context and enrich them:

.. code-block:: python

   q = Query(kidney_terms, force_fail=True)
   enriched = q.contextual_slim_enrichment(["UBERON:0000362"])  # renal medulla

Parent-only Enrichment
----------------------

Use :meth:`pandasaurus.query.Query.parent_enrichment` for a one-hop graph:

.. code-block:: python

   q = Query(seeds)
   parent_df = q.parent_enrichment()

Export to Graph
---------------

After any enrichment call:

.. code-block:: python

   graph_df = q.graph_df  # pandas DataFrame
   rdflib_graph = q.graph

Use :mod:`pandasaurus.graph.graph_generator` to further manipulate the graph or export as needed.
