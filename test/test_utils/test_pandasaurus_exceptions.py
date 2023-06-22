import pytest

from pandasaurus.resources.term import Term
from pandasaurus.utils.pandasaurus_exceptions import InvalidTerm, ObsoletedTerm


def test_invalid_term_exception():
    term_list = [Term("T cell", "CL:0000084", True), Term("memory B celll", "CL:0000787", True)]
    with pytest.raises(InvalidTerm) as exc_info:
        raise InvalidTerm(term_list)

    exception = exc_info.value
    assert exception.term_list == term_list
    expected_message = "The following terms are invalid: CL:0000084, CL:0000787"
    assert str(exception) == expected_message


def test_obsoleted_term_exception():
    term_list = [Term("obsolete Muller cell", "CL:0011107", True, "Mueller cell", "CL:0000636")]
    with pytest.raises(ObsoletedTerm) as exc_info:
        raise ObsoletedTerm(term_list)

    exception = exc_info.value
    assert exception.term_list == term_list
    expected_message = (
        "The following terms are obsoleted: CL:0011107, and replaced by following terms: CL:0000636. "
        "Please consider using the new terms"
    )
    assert str(exception) == expected_message
