from typing import Dict, List
from unittest.mock import patch
import pytest

from pandasaurus.curie_validator import CurieValidator
from pandasaurus.resources.term import Term
from pandasaurus.utils.pandasaurus_exceptions import InvalidTerm, ObsoletedTerm


def test_validate_curie_prefixes():
    pass


def test_validate_curie_list():
    curie_list_test_data = ["CL:0002681", "CL:0002518", "CL:1234567", "CL:1000500"]

    expected_validate_curie_list = {
        "CL:0002681": {"label": "kidney cortical cell", "valid": True},
        "CL:0002518": {"label": "kidney epithelial cell", "valid": True},
        "CL:1234567": {"label": None, "valid": False},
        "CL:1000500": {"label": "kidney interstitial cell", "valid": True},
    }

    validate_curie_list = CurieValidator.validate_curie_list(curie_list_test_data)
    assert validate_curie_list == expected_validate_curie_list


def test_find_obsolete_terms():
    find_obsolete_term_test_data = ["CL:0000337", "CL:0011107", "CL:0002371", "CL:0002150"]

    expected_find_obsolete_terms = {
        "CL:0011107": {
            "term": "CL:0011107",
            "depr_status": "true",
            "new_term": "CL:0000636",
            "label": "obsolete Muller cell",
            "new_term_label": "Mueller cell",
        }
    }

    find_obsolete_terms = CurieValidator.find_obsolete_terms(find_obsolete_term_test_data)
    assert find_obsolete_terms == expected_find_obsolete_terms


def test_find_obsolete_term_replacement():
    pass


def test_get_validation_report():
    report_none = CurieValidator.get_validation_report([Term("T cell", "CL:0000084", True)])
    assert report_none is None
    # TODO add test cases for invalid and obsoleted terms


def test_construct_term_list():
    construct_term_list_test_data = ["CL:0000084", "CL:0000787", "CL:0000788", "CL:0000798"]
    expected_construct_term_list = [
        Term("T cell", "CL:0000084", True),
        Term("memory B cell", "CL:0000787", True),
        Term("naive B cell", "CL:0000788", True),
        Term("gamma-delta T cell", "CL:0000798", True),
    ]

    construct_term_list = CurieValidator.construct_term_list(construct_term_list_test_data)
    assert construct_term_list == expected_construct_term_list
