import pytest

from pandasaurus.resources.term import Term
from pandasaurus.utils.pandasaurus_exceptions import (
    EnrichedDataFrameEmpty,
    InvalidOntology,
    InvalidTerm,
    ObsoletedTerm,
)


def test_invalid_term_exception():
    term_list = [Term("T cell", "CL:0000084", True), Term("memory B celll", "CL:0000787", True)]
    with pytest.raises(InvalidTerm) as exc_info:
        raise InvalidTerm(term_list)

    expected_message = "The following terms are invalid: CL:0000084, CL:0000787"
    assert str(exc_info.value) == expected_message


def test_obsoleted_term_exception():
    term_list = [Term("obsolete Muller cell", "CL:0011107", True, "Mueller cell", "CL:0000636")]
    with pytest.raises(ObsoletedTerm) as exc_info:
        raise ObsoletedTerm(term_list)

    expected_message = (
        "The following terms are obsoleted: CL:0011107, and replaced by following terms: CL:0000636. "
        "Please consider using the new terms"
    )
    assert str(exc_info.value) == expected_message


def test_enriched_dataframe_empty_exception():
    with pytest.raises(EnrichedDataFrameEmpty) as exc_info:
        raise EnrichedDataFrameEmpty()

    expected_message = (
        "The enriched DataFrame cannot be empty for synonym lookup. Please use an enrichment method " "first"
    )
    assert str(exc_info.value) == expected_message


def test_invalid_ontology_exception():
    input_ontology = "Cel Ontology"
    ontology_list = ["Cell Ontology", "Mondo Disease Ontology", "Uber-anatomy ontology"]
    with pytest.raises(InvalidOntology) as exc_info:
        raise InvalidOntology(input_ontology, ontology_list)
    expected_message = (
        f"The '{input_ontology}' ontology is invalid. \nPlease use one of the following ontologies: "
        f"\nCell Ontology, Mondo Disease Ontology, Uber-anatomy ontology"
    )
    assert expected_message in str(exc_info.value)
