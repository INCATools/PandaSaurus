from test.data.curie_validator_data import (
    get_construct_term_list_data,
    get_construct_term_list_missing_validation_data,
    get_construct_term_list_missing_validation_result,
    get_construct_term_list_result,
    get_expected_construct_term_list,
    get_expected_construct_term_list_missing_validation,
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


def test_validate_curie_list_batches_requests(mocker):
    mocker.patch.object(CurieValidator, "_CURIE_CHUNK_SIZE", 2)
    run_query_mock = mocker.patch(
        "pandasaurus.curie_validator.run_sparql_query",
        side_effect=[
            iter(
                [
                    {"label": "kidney epithelial cell", "term": "CL:0002518"},
                    {"label": "kidney cortical cell", "term": "CL:0002681"},
                ]
            ),
            iter([{"label": "kidney interstitial cell", "term": "CL:1000500"}]),
        ],
    )
    curie_list = ["CL:0002518", "CL:0002681", "CL:1000500", "CL:1234567"]

    result = CurieValidator.validate_curie_list(curie_list)

    assert run_query_mock.call_count == 2
    assert result == {
        "CL:0002518": {"label": "kidney epithelial cell", "valid": True},
        "CL:0002681": {"label": "kidney cortical cell", "valid": True},
        "CL:1000500": {"label": "kidney interstitial cell", "valid": True},
        "CL:1234567": {"label": None, "valid": False},
    }


def test_find_obsolete_terms(mocker):
    mocker.patch(
        "pandasaurus.curie_validator.run_sparql_query",
        side_effect=[
            iter(get_find_obsolete_terms_result()),
        ],
    )

    assert CurieValidator.find_obsolete_terms(get_find_obsolete_terms_data()) == get_expected_find_obsolete_terms()


def test_find_obsolete_terms_batches_requests(mocker):
    mocker.patch.object(CurieValidator, "_CURIE_CHUNK_SIZE", 2)
    run_query_mock = mocker.patch(
        "pandasaurus.curie_validator.run_sparql_query",
        side_effect=[
            iter(
                [
                    {
                        "depr_status": "true",
                        "label": "obsolete Muller cell",
                        "new_term": "CL:0000636",
                        "new_term_label": "Mueller cell",
                        "term": "CL:0011107",
                    }
                ]
            ),
            iter([]),
        ],
    )
    curie_list = ["CL:0011107", "CL:0000337", "CL:0002371"]

    result = CurieValidator.find_obsolete_terms(curie_list)

    assert run_query_mock.call_count == 2
    assert result == {
        "CL:0011107": {
            "term": "CL:0011107",
            "depr_status": "true",
            "new_term": "CL:0000636",
            "label": "obsolete Muller cell",
            "new_term_label": "Mueller cell",
        }
    }


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
        "The following terms are obsoleted: CL:0011107. "
        "Replacement suggestions: CL:0011107 -> CL:0000636. "
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


def test_construct_term_list_handles_missing_validation(mocker):
    mocker.patch(
        "pandasaurus.curie_validator.run_sparql_query",
        side_effect=[
            iter(get_construct_term_list_missing_validation_result()),
            iter([]),
        ],
    )

    assert (
        CurieValidator.construct_term_list(get_construct_term_list_missing_validation_data())
        == get_expected_construct_term_list_missing_validation()
    )
