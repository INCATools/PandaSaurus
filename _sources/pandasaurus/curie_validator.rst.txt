Curie Validator
==================

Overview
--------

``CurieValidator`` validates seed CURIEs and surfaces obsoleted terms in a structured way. Use it before running any enrichment to ensure your data is clean.

Typical usage:

.. code-block:: python

   terms = CurieValidator.construct_term_list(seeds)
   CurieValidator.get_validation_report(terms)  # raises on invalid/obsoleted terms

Class Reference
---------------

.. currentmodule:: pandasaurus.curie_validator

.. autoclass:: CurieValidator
   :members:
