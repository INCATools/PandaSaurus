from pandasaurus.resources.term import Term


def test_get_label():
    term = Term("T cell", "CL:0000084", True)
    assert term.get_label() == "T cell"


def test_get_iri():
    term = Term("T cell", "CL:0000084", True)
    assert term.get_iri() == "CL:0000084"


def test_get_is_valid():
    term = Term("T cell", "CL:0000084", True)
    assert term.get_is_valid() is True


def test_get_new_label():
    term = Term("obsolete Muller cell", "CL:0011107", True, "Muller cell", "CL:0000636")
    assert term.get_new_label() == "Muller cell"


def test_get_new_iri():
    term = Term("obsolete Muller cell", "CL:0011107", True, "Muller cell", "CL:0000636")
    assert term.get_new_iri() == "CL:0000636"


def test_get_is_obsoleted():
    term = Term("T cell", "CL:0000084", True)
    assert term.get_is_obsoleted() is False


def test_update_obsoleted_term():
    term = Term("obsolete Muller cell", "CL:0011107", True, "Muller cell", "CL:0000636")
    term.update_obsoleted_term()
    assert term.get_is_obsoleted() is False
    assert term.get_label() == "Muller cell"
    assert term.get_iri() == "CL:0000636"


def test_eq():
    term1 = Term("T cell", "CL:0000084", True)
    term2 = Term("T cell", "CL:0000084", True)
    term3 = Term("T cell", "CL:00000841", True)
    term4 = "term"
    assert term1 == term2
    assert term1 != term3
    assert term2 != term4


def test_str():
    term = Term("T cell", "CL:0000084", True)
    assert str(term) == "IRI: CL:0000084, Label: T cell, Valid: True, Obsoleted: False"
    obsolete_term = Term("obsolete Muller cell", "CL:0011107", True, "Muller cell", "CL:0000636")
    assert (
        str(obsolete_term) == "IRI: CL:0011107, Label: obsolete Muller cell, Valid: True, Obsoleted: True, "
        "New term label: Muller cell, New term IRI: CL:0000636"
    )
