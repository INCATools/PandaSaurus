import pytest

from src.pandasaurus.utils.query_utils import chunks, get_prefixes, run_sparql_query


def test_run_sparql_query():
    query = "SELECT * WHERE {?s ?p ?o} LIMIT 1"
    result = run_sparql_query(query)
    try:
        element = next(result)
        assert element is not None
    except StopIteration:
        pytest.fail("Iterator should have at least one element")


def test_chunks():
    lst = [1, 2, 3, 4, 5, 6]
    n = 2
    result = list(chunks(lst, n))
    assert len(result) == 3
    assert result == [[1, 2], [3, 4], [5, 6]]


def test_get_prefixes():
    text = (
        "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX CL: <http://purl.obolibrary.org/obo/CL_> "
        "PREFIX owl: <http://www.w3.org/2002/07/owl#> PREFIX UBERON: <http://purl.obolibrary.org/obo/UBERON_> "
        "PREFIX BFO: <http://purl.obolibrary.org/obo/BFO_> SELECT * WHERE {?s ?p ?o}"
    )
    prefix_map = {
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "CL": "http://purl.obolibrary.org/obo/CL_",
        "owl": "http://www.w3.org/2002/07/owl#",
        "UBERON": "http://purl.obolibrary.org/obo/UBERON_",
        "BFO": "http://purl.obolibrary.org/obo/BFO_",
    }
    result = get_prefixes(text, prefix_map)
    assert result == ["rdfs", "CL", "owl", "UBERON", "BFO"]
