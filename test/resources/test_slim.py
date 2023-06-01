from pandasaurus.resources.slim import Slim
from pandasaurus.resources.term import Term


def test_get_name():
    slim = Slim(
        "blood_and_immune_upper_slim",
        "a subset of general classes related to blood and the immune system, primarily of hematopoietic origin",
    )
    assert slim.get_name() == "blood_and_immune_upper_slim"


def test_get_description():
    slim = Slim(
        "blood_and_immune_upper_slim",
        "a subset of general classes related to blood and the immune system, primarily of hematopoietic origin",
    )
    assert (
        slim.get_description()
        == "a subset of general classes related to blood and the immune system, primarily of hematopoietic origin"
    )


def test_get_term_list():
    term_list = [
        Term("T cell", "CL:0000084", True),
        Term("memory B cell", "CL:0000787", True),
        Term("naive B cell", "CL:0000788", True),
        Term("gamma-delta T cell", "CL:0000798", True),
    ]
    slim = Slim(
        "blood_and_immune_upper_slim",
        "a subset of general classes related to blood and the immune system, primarily of hematopoietic origin",
        term_list,
    )
    assert slim.get_term_list() == term_list


def test_set_term_list():
    term_list = [
        Term("T cell", "CL:0000084", True),
        Term("memory B cell", "CL:0000787", True),
        Term("naive B cell", "CL:0000788", True),
        Term("gamma-delta T cell", "CL:0000798", True),
    ]
    slim = Slim(
        "blood_and_immune_upper_slim",
        "a subset of general classes related to blood and the immune system, primarily of hematopoietic origin",
    )
    slim.set_term_list(term_list)
    assert slim.get_term_list() == term_list


def test_str():
    slim = Slim(
        "blood_and_immune_upper_slim",
        "a subset of general classes related to blood and the immune system, primarily of hematopoietic origin",
    )
    assert (
        str(slim)
        == "Name:blood_and_immune_upper_slim, Description: a subset of general classes related to blood and the "
        "immune system, primarily of hematopoietic origin"
    )
