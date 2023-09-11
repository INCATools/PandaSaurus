from test.data.query_data import (
    get_ancestor_enrichment_data,
    get_ancestor_enrichment_result,
    get_ancestor_object_list,
    get_blood_and_immune_test_data,
    get_context_list,
    get_context_members_result,
    get_contextual_enrichment_data,
    get_contextual_enrichment_result,
    get_enrichment_find_obsolete_terms_data,
    get_enrichment_validate_curie_list_result,
    get_full_enrichment_data,
    get_full_enrichment_result,
    get_kidney_test_data,
    get_minimal_enrichment_data,
    get_minimal_enrichment_result,
    get_simple_enrichment_data,
    get_simple_enrichment_result,
    get_synonym_lookup_data,
    get_synonym_lookup_result,
)
from test.data.slim_manager_data import get_slim_list, get_slim_members_result

import pandas as pd
import pytest

from pandasaurus.query import Query
from pandasaurus.utils.query_utils import run_sparql_query
from pandasaurus.utils.sparql_queries import get_contextual_enrichment_query

blood_and_immune_test_data = get_blood_and_immune_test_data()

kidney_test_data = get_kidney_test_data()

slim_list = get_slim_list()
context_list = get_context_list()  # renal medulla


def test_query_constructor_with_valid_seed_list(mocker):
    seed_list = ["CL:0000084", "CL:0000787"]
    mocker.patch(
        "pandasaurus.curie_validator.run_sparql_query",
        side_effect=[
            iter([{"label": "T cell", "term": "CL:0000084"}, {"label": "memory B cell", "term": "CL:0000787"}]),
            iter([]),
        ],
    )
    query = Query(seed_list)
    assert query is not None


def test_query_constructor_with_invalid_seed_list(mocker):
    seed_list = ["CL:0000084", "CL:1234567"]
    mocker.patch(
        "pandasaurus.curie_validator.run_sparql_query",
        side_effect=[
            iter([{"label": "T cell", "term": "CL:0000084"}]),
            iter([]),
        ],
    )
    with pytest.raises(ValueError) as exc_info:
        Query(seed_list, force_fail=True)

    exception = exc_info.value
    assert isinstance(exception, ValueError)
    expected_message = "Check your seed list! It contains invalid terms"
    assert str(exception) == expected_message


def test_query_constructor_with_obsoleted_seed_list(mocker):
    seed_list = ["CL:0000084", "CL:0011107"]
    mocker.patch(
        "pandasaurus.curie_validator.run_sparql_query",
        side_effect=[
            iter([{"label": "T cell", "term": "CL:0000084"}, {"label": "obsolete Muller cell", "term": "CL:0011107"}]),
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
        ],
    )
    with pytest.raises(ValueError) as exc_info:
        Query(seed_list, force_fail=True)

    exception = exc_info.value
    assert isinstance(exception, ValueError)
    expected_message = (
        "Check your seed list! It contains obsoleted terms. Use update_obsoleted_terms method to update all "
        "obsoleted term"
    )
    assert str(exception) == expected_message


def test_simple_enrichment(mocker):
    expected_simple_df = pd.DataFrame(
        get_simple_enrichment_data(), columns=["s", "s_label", "p", "o", "o_label"]
    ).sort_values("s")

    mocker.patch(
        "pandasaurus.curie_validator.run_sparql_query",
        side_effect=[
            iter(get_enrichment_validate_curie_list_result()),
            iter(get_enrichment_find_obsolete_terms_data()),
        ],
    )
    # TODO Second call has to be revised
    mocker.patch(
        "pandasaurus.query.run_sparql_query",
        side_effect=[
            iter(get_simple_enrichment_result()),
            iter(get_simple_enrichment_result()),
        ],
    )
    q = Query(blood_and_immune_test_data)
    df = q.simple_enrichment()
    assert df["s"].isin(blood_and_immune_test_data).any()
    assert df["o"].isin(blood_and_immune_test_data).any()
    assert expected_simple_df["s"].reset_index(drop=True).equals(df["s"].reset_index(drop=True))
    assert expected_simple_df["o"].reset_index(drop=True).equals(df["o"].reset_index(drop=True))


def test_minimal_slim_enrichment(mocker):
    expected_minimal_slim_df = pd.DataFrame(
        get_minimal_enrichment_data(), columns=["s", "s_label", "p", "o", "o_label"]
    ).sort_values("s")

    mocker.patch(
        "pandasaurus.curie_validator.run_sparql_query",
        side_effect=[
            iter(get_enrichment_validate_curie_list_result()),
            iter(get_enrichment_find_obsolete_terms_data()),
        ],
    )
    mocker.patch(
        "pandasaurus.slim_manager.run_sparql_query",
        side_effect=[
            iter(get_slim_members_result()),
        ],
    )
    # TODO refactor needed!!!
    mocker.patch(
        "pandasaurus.query.run_sparql_query",
        side_effect=[
            iter(get_minimal_enrichment_result()),
            iter(get_minimal_enrichment_result()),
            iter(get_minimal_enrichment_result()),
            iter(get_minimal_enrichment_result()),
            iter(get_minimal_enrichment_result()),
        ],
    )
    q = Query(blood_and_immune_test_data)
    df = q.minimal_slim_enrichment(slim_list)
    assert df["s"].isin(blood_and_immune_test_data).any()
    assert df["o"].isin(blood_and_immune_test_data).any()
    assert expected_minimal_slim_df["s"].reset_index(drop=True).equals(df["s"].reset_index(drop=True))
    assert (
        expected_minimal_slim_df["o"]
        .sort_values()
        .reset_index(drop=True)
        .equals(df["o"].sort_values().reset_index(drop=True))
    )


def test_full_slim_enrichment(mocker):
    expected_full_slim_df = pd.DataFrame(
        get_full_enrichment_data(), columns=["s", "s_label", "p", "o", "o_label"]
    ).sort_values("s")

    mocker.patch(
        "pandasaurus.curie_validator.run_sparql_query",
        side_effect=[
            iter(get_enrichment_validate_curie_list_result()),
            iter(get_enrichment_find_obsolete_terms_data()),
        ],
    )
    mocker.patch(
        "pandasaurus.slim_manager.run_sparql_query",
        side_effect=[
            iter(get_slim_members_result()),
        ],
    )
    # TODO refactor needed!!!
    mocker.patch(
        "pandasaurus.query.run_sparql_query",
        side_effect=[
            iter(get_full_enrichment_result()),
            iter(get_full_enrichment_result()),
            iter(get_full_enrichment_result()),
            iter(get_full_enrichment_result()),
            iter(get_full_enrichment_result()),
        ],
    )
    q = Query(blood_and_immune_test_data)
    df = q.full_slim_enrichment(slim_list)
    assert df["s"].isin(blood_and_immune_test_data).any()
    assert df["o"].isin(blood_and_immune_test_data).any()
    assert expected_full_slim_df["s"].reset_index(drop=True).equals(df["s"].reset_index(drop=True))
    assert (
        expected_full_slim_df["o"]
        .sort_values()
        .reset_index(drop=True)
        .equals(df["o"].sort_values().reset_index(drop=True))
    )


def test_contextual_slim_enrichment(mocker):
    expected_contextual_df = pd.DataFrame(
        get_contextual_enrichment_data(), columns=["s", "s_label", "p", "o", "o_label"]
    ).sort_values("s")

    mocker.patch(
        "pandasaurus.curie_validator.run_sparql_query",
        side_effect=[
            iter(get_enrichment_validate_curie_list_result()),
            iter(get_enrichment_find_obsolete_terms_data()),
        ],
    )
    # TODO refactor needed!!!
    mocker.patch(
        "pandasaurus.query.run_sparql_query",
        side_effect=[
            iter(get_context_members_result()),
            iter(get_contextual_enrichment_result()[0:89]),
            iter(get_contextual_enrichment_result()[90:113]),
            iter(get_contextual_enrichment_result()),
            iter(get_contextual_enrichment_result()),
            iter(get_contextual_enrichment_result()),
            iter(get_contextual_enrichment_result()),
            iter(get_contextual_enrichment_result()),
            iter(get_contextual_enrichment_result()),
            iter(get_contextual_enrichment_result()),
            iter(get_contextual_enrichment_result()),
            iter(get_contextual_enrichment_result()),
        ],
    )
    q = Query(kidney_test_data)
    df = q.contextual_slim_enrichment(context_list)
    query_string = get_contextual_enrichment_query(context_list)
    object_list = kidney_test_data + [res.get("term") for res in run_sparql_query(query_string)]
    assert df["s"].isin(kidney_test_data).any()
    assert df["o"].isin(object_list).any()
    assert expected_contextual_df["s"].reset_index(drop=True).equals(df["s"].reset_index(drop=True))
    assert (
        expected_contextual_df["o"]
        .sort_values()
        .reset_index(drop=True)
        .equals(df["o"].sort_values().reset_index(drop=True))
    )


def test_ancestor_enrichment(mocker):
    expected_simple_df = pd.DataFrame(
        get_ancestor_enrichment_data(), columns=["s", "s_label", "p", "o", "o_label"]
    ).sort_values("s")

    mocker.patch(
        "pandasaurus.curie_validator.run_sparql_query",
        side_effect=[
            iter(get_enrichment_validate_curie_list_result()),
            iter(get_enrichment_find_obsolete_terms_data()),
        ],
    )
    mocker.patch(
        "pandasaurus.query.run_sparql_query",
        side_effect=[
            iter(get_ancestor_object_list()),
            iter(get_ancestor_enrichment_result()),
            iter(get_ancestor_enrichment_result()),
        ],
    )
    q = Query(blood_and_immune_test_data)
    df = q.ancestor_enrichment(2)
    assert df["s"].isin(blood_and_immune_test_data).any()
    assert df["o"].isin(blood_and_immune_test_data).any()
    assert expected_simple_df["s"].reset_index(drop=True).equals(df["s"].reset_index(drop=True))
    assert expected_simple_df["o"].reset_index(drop=True).equals(df["o"].reset_index(drop=True))


def test_synonym_lookup(mocker):
    q = Query(["CL:0000084", "CL:0000813", "CL:0000815", "CL:0000900"])

    mocker.patch(
        "pandasaurus.query.run_sparql_query",
        side_effect=[
            iter(get_synonym_lookup_result()),
        ],
    )

    result_df = q.synonym_lookup()
    expected_df = pd.DataFrame(get_synonym_lookup_data())
    pd.testing.assert_frame_equal(result_df, expected_df)


def test_query():
    pass


def test_update_obsoleted_terms():
    seed_list = ["CL:0000084", "CL:0011107"]
    expected_update_obsoleted_terms = [
        "IRI: CL:0000084, Label: T cell, Valid: True, Obsoleted: False",
        "IRI: CL:0000636, Label: Mueller cell, Valid: True, Obsoleted: False",
    ]
    q = Query(seed_list)
    q.update_obsoleted_terms()
    assert [str(term) for term in q._Query__term_list] == expected_update_obsoleted_terms
