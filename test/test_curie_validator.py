from test.data.curie_validator_data import (
    get_construct_term_list_data,
    get_construct_term_list_result,
    get_expected_construct_term_list,
    get_expected_find_obsolete_terms,
    get_expected_validate_curie_list,
    get_find_obsolete_terms_data,
    get_find_obsolete_terms_result,
    get_validate_curie_list_data,
    get_validate_curie_list_result,
)

import pytest

from pandasaurus.curie_validator import CurieValidator
from pandasaurus.resources.term import Term
from pandasaurus.utils.pandasaurus_exceptions import InvalidTerm, ObsoletedTerm


def test_validate_curie_prefixes():
    pass


def test_validate_curie_list(mocker):
    mocker.patch(
        "pandasaurus.curie_validator.run_sparql_query",
        side_effect=[iter(get_validate_curie_list_result())],
    )

    assert CurieValidator.validate_curie_list(get_validate_curie_list_data()) == get_expected_validate_curie_list()


def test_find_obsolete_terms(mocker):
    mocker.patch(
        "pandasaurus.curie_validator.run_sparql_query",
        side_effect=[
            iter(get_find_obsolete_terms_result()),
        ],
    )

    assert CurieValidator.find_obsolete_terms(get_find_obsolete_terms_data()) == get_expected_find_obsolete_terms()


def test_find_obsolete_term_replacement():
    pass


def test_get_validation_report():
    term_list = [Term("T cell", "CL:0000084", True)]
    report_none = CurieValidator.get_validation_report(term_list)
    assert report_none is None

    term_list = [Term("xxx cell", "CL:1234567", False)]
    with pytest.raises(InvalidTerm) as exc_info:
        CurieValidator.get_validation_report(term_list)

    assert str(exc_info.value) == "The following terms are invalid: CL:1234567"

    term_list = [Term("obsolete Muller cell", "CL:0011107", True, "Mueller cell", "CL:0000636")]
    with pytest.raises(ObsoletedTerm) as exc_info:
        CurieValidator.get_validation_report(term_list)

    expected_message = (
        "The following terms are obsoleted: CL:0011107, and replaced by following terms: CL:0000636. "
        "Please consider using the new terms"
    )
    assert str(exc_info.value) == expected_message


def test_construct_term_list(mocker):
    mocker.patch(
        "pandasaurus.curie_validator.run_sparql_query",
        side_effect=[
            iter(get_construct_term_list_result()),
            iter([]),
        ],
    )

    assert CurieValidator.construct_term_list(get_construct_term_list_data()) == get_expected_construct_term_list()
