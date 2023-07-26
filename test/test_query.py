import pandas as pd
import pytest

from pandasaurus.query import Query
from pandasaurus.utils.query_utils import run_sparql_query
from pandasaurus.utils.sparql_queries import get_contextual_enrichment_query

blood_and_immune_test_data = [
    "CL:0000084",
    "CL:0000787",
    "CL:0000788",
    "CL:0000798",
    "CL:0000809",
    "CL:0000813",
    "CL:0000815",
    "CL:0000895",
    "CL:0000897",
    "CL:0000900",
    "CL:0000909",
    "CL:0000940",
    "CL:0000980",
    "CL:0002489",
]

kidney_test_data = [
    "CL:0000115",
    "CL:0000653",
    "CL:0000738",
    "CL:0002306",
    "CL:0002319",
    "CL:1000452",
    "CL:1000597",
    "CL:1000692",
    "CL:1000768",
    "CL:1000849",
    "CL:1001108",
    "CL:1001107",
    "CL:1001111",
    "CL:1001318",
    "CL:1001431",
    "CL:1001432",
]

slim_list = ["blood_and_immune_upper_slim"]
context_list = ["UBERON:0000362"]  # renal medulla


def test_query_constructor_with_valid_seed_list():
    seed_list = ["CL:0000084", "CL:0000787"]
    query = Query(seed_list)
    assert query is not None


def test_query_constructor_with_invalid_seed_list():
    seed_list = ["CL:0000084", "CL:1234567"]
    with pytest.raises(ValueError) as exc_info:
        Query(seed_list, force_fail=True)

    exception = exc_info.value
    assert type(exception) == ValueError
    expected_message = "Check your seed list! It contains invalid terms"
    assert str(exception) == expected_message


def test_query_constructor_with_obsoleted_seed_list():
    seed_list = ["CL:0000084", "CL:0011107"]
    with pytest.raises(ValueError) as exc_info:
        Query(seed_list, force_fail=True)

    exception = exc_info.value
    assert type(exception) == ValueError
    expected_message = (
        "Check your seed list! It contains obsoleted terms. Use update_obsoleted_terms method to update all "
        "obsoleted term"
    )
    assert str(exception) == expected_message


def test_simple_enrichment():
    data_simple = [
        {
            "s": "CL:0000798",
            "s_label": "gamma-delta T cell",
            "p": "rdfs:subClassOf",
            "o": "CL:0000084",
            "o_label": "T cell",
        },
        {
            "s": "CL:0000809",
            "s_label": "double-positive, alpha-beta thymocyte",
            "p": "rdfs:subClassOf",
            "o": "CL:0000084",
            "o_label": "T cell",
        },
        {
            "s": "CL:0000813",
            "s_label": "memory T cell",
            "p": "rdfs:subClassOf",
            "o": "CL:0000084",
            "o_label": "T cell",
        },
        {
            "s": "CL:0000815",
            "s_label": "regulatory T cell",
            "p": "rdfs:subClassOf",
            "o": "CL:0000084",
            "o_label": "T cell",
        },
        {
            "s": "CL:0000895",
            "s_label": "naive thymus-derived CD4-positive, alpha-beta T cell",
            "p": "rdfs:subClassOf",
            "o": "CL:0000084",
            "o_label": "T cell",
        },
        {
            "s": "CL:0000897",
            "s_label": "CD4-positive, alpha-beta memory T cell",
            "p": "rdfs:subClassOf",
            "o": "CL:0000084",
            "o_label": "T cell",
        },
        {
            "s": "CL:0000900",
            "s_label": "naive thymus-derived CD8-positive, alpha-beta T cell",
            "p": "rdfs:subClassOf",
            "o": "CL:0000084",
            "o_label": "T cell",
        },
        {
            "s": "CL:0000909",
            "s_label": "CD8-positive, alpha-beta memory T cell",
            "p": "rdfs:subClassOf",
            "o": "CL:0000084",
            "o_label": "T cell",
        },
        {
            "s": "CL:0000940",
            "s_label": "mucosal invariant T cell",
            "p": "rdfs:subClassOf",
            "o": "CL:0000084",
            "o_label": "T cell",
        },
        {
            "s": "CL:0002489",
            "s_label": "double negative thymocyte",
            "p": "rdfs:subClassOf",
            "o": "CL:0000084",
            "o_label": "T cell",
        },
        {
            "s": "CL:0000897",
            "s_label": "CD4-positive, alpha-beta memory T cell",
            "p": "rdfs:subClassOf",
            "o": "CL:0000813",
            "o_label": "memory T cell",
        },
        {
            "s": "CL:0000909",
            "s_label": "CD8-positive, alpha-beta memory T cell",
            "p": "rdfs:subClassOf",
            "o": "CL:0000813",
            "o_label": "memory T cell",
        },
    ]
    expected_simple_df = pd.DataFrame(data_simple, columns=["s", "s_label", "p", "o", "o_label"]).sort_values("s")

    q = Query(blood_and_immune_test_data)
    df = q.simple_enrichment()
    assert df["s"].isin(blood_and_immune_test_data).any()
    assert df["o"].isin(blood_and_immune_test_data).any()
    assert expected_simple_df["s"].reset_index(drop=True).equals(df["s"].reset_index(drop=True))
    assert expected_simple_df["o"].reset_index(drop=True).equals(df["o"].reset_index(drop=True))


def test_minimal_slim_enrichment():
    data_minimal_slim = [
        {
            "s": "CL:0000084",
            "s_label": "T cell",
            "p": "rdfs:subClassOf",
            "o": "CL:0000842",
            "o_label": "mononuclear cell",
        },
        {
            "s": "CL:0000787",
            "s_label": "memory B cell",
            "p": "rdfs:subClassOf",
            "o": "CL:0000145",
            "o_label": "professional antigen presenting cell",
        },
        {
            "s": "CL:0000787",
            "s_label": "memory B cell",
            "p": "rdfs:subClassOf",
            "o": "CL:0000236",
            "o_label": "B cell",
        },
        {
            "s": "CL:0000787",
            "s_label": "memory B cell",
            "p": "rdfs:subClassOf",
            "o": "CL:0000842",
            "o_label": "mononuclear cell",
        },
        {
            "s": "CL:0000788",
            "s_label": "naive B cell",
            "p": "rdfs:subClassOf",
            "o": "CL:0000236",
            "o_label": "B cell",
        },
        {
            "s": "CL:0000788",
            "s_label": "naive B cell",
            "p": "rdfs:subClassOf",
            "o": "CL:0000842",
            "o_label": "mononuclear cell",
        },
        {
            "s": "CL:0000788",
            "s_label": "naive B cell",
            "p": "rdfs:subClassOf",
            "o": "CL:0000145",
            "o_label": "professional antigen presenting cell",
        },
        {
            "s": "CL:0000798",
            "s_label": "gamma-delta T cell",
            "p": "rdfs:subClassOf",
            "o": "CL:0000842",
            "o_label": "mononuclear cell",
        },
        {
            "s": "CL:0000798",
            "s_label": "gamma-delta T cell",
            "p": "rdfs:subClassOf",
            "o": "CL:0000084",
            "o_label": "T cell",
        },
        {
            "s": "CL:0000809",
            "s_label": "double-positive, alpha-beta thymocyte",
            "p": "rdfs:subClassOf",
            "o": "CL:0000789",
            "o_label": "alpha-beta T cell",
        },
        {
            "s": "CL:0000809",
            "s_label": "double-positive, alpha-beta thymocyte",
            "p": "rdfs:subClassOf",
            "o": "CL:0000842",
            "o_label": "mononuclear cell",
        },
        {
            "s": "CL:0000809",
            "s_label": "double-positive, alpha-beta thymocyte",
            "p": "rdfs:subClassOf",
            "o": "CL:0002420",
            "o_label": "immature T cell",
        },
        {
            "s": "CL:0000809",
            "s_label": "double-positive, alpha-beta thymocyte",
            "p": "rdfs:subClassOf",
            "o": "CL:0000084",
            "o_label": "T cell",
        },
        {
            "s": "CL:0000813",
            "s_label": "memory T cell",
            "p": "rdfs:subClassOf",
            "o": "CL:0000084",
            "o_label": "T cell",
        },
        {
            "s": "CL:0000813",
            "s_label": "memory T cell",
            "p": "rdfs:subClassOf",
            "o": "CL:0000842",
            "o_label": "mononuclear cell",
        },
        {
            "s": "CL:0000815",
            "s_label": "regulatory T cell",
            "p": "rdfs:subClassOf",
            "o": "CL:0000084",
            "o_label": "T cell",
        },
        {
            "s": "CL:0000815",
            "s_label": "regulatory T cell",
            "p": "rdfs:subClassOf",
            "o": "CL:0000842",
            "o_label": "mononuclear cell",
        },
        {
            "s": "CL:0000895",
            "s_label": "naive thymus-derived CD4-positive, alpha-beta T cell",
            "p": "rdfs:subClassOf",
            "o": "CL:0000842",
            "o_label": "mononuclear cell",
        },
        {
            "s": "CL:0000895",
            "s_label": "naive thymus-derived CD4-positive, alpha-beta T cell",
            "p": "rdfs:subClassOf",
            "o": "CL:0000789",
            "o_label": "alpha-beta T cell",
        },
        {
            "s": "CL:0000895",
            "s_label": "naive thymus-derived CD4-positive, alpha-beta T cell",
            "p": "rdfs:subClassOf",
            "o": "CL:0000084",
            "o_label": "T cell",
        },
        {
            "s": "CL:0000897",
            "s_label": "CD4-positive, alpha-beta memory T cell",
            "p": "rdfs:subClassOf",
            "o": "CL:0000813",
            "o_label": "memory T cell",
        },
        {
            "s": "CL:0000897",
            "s_label": "CD4-positive, alpha-beta memory T cell",
            "p": "rdfs:subClassOf",
            "o": "CL:0000084",
            "o_label": "T cell",
        },
        {
            "s": "CL:0000897",
            "s_label": "CD4-positive, alpha-beta memory T cell",
            "p": "rdfs:subClassOf",
            "o": "CL:0000789",
            "o_label": "alpha-beta T cell",
        },
        {
            "s": "CL:0000897",
            "s_label": "CD4-positive, alpha-beta memory T cell",
            "p": "rdfs:subClassOf",
            "o": "CL:0000842",
            "o_label": "mononuclear cell",
        },
        {
            "s": "CL:0000900",
            "s_label": "naive thymus-derived CD8-positive, alpha-beta T cell",
            "p": "rdfs:subClassOf",
            "o": "CL:0000084",
            "o_label": "T cell",
        },
        {
            "s": "CL:0000900",
            "s_label": "naive thymus-derived CD8-positive, alpha-beta T cell",
            "p": "rdfs:subClassOf",
            "o": "CL:0000789",
            "o_label": "alpha-beta T cell",
        },
        {
            "s": "CL:0000900",
            "s_label": "naive thymus-derived CD8-positive, alpha-beta T cell",
            "p": "rdfs:subClassOf",
            "o": "CL:0000842",
            "o_label": "mononuclear cell",
        },
        {
            "s": "CL:0000909",
            "s_label": "CD8-positive, alpha-beta memory T cell",
            "p": "rdfs:subClassOf",
            "o": "CL:0000842",
            "o_label": "mononuclear cell",
        },
        {
            "s": "CL:0000909",
            "s_label": "CD8-positive, alpha-beta memory T cell",
            "p": "rdfs:subClassOf",
            "o": "CL:0000084",
            "o_label": "T cell",
        },
        {
            "s": "CL:0000909",
            "s_label": "CD8-positive, alpha-beta memory T cell",
            "p": "rdfs:subClassOf",
            "o": "CL:0000789",
            "o_label": "alpha-beta T cell",
        },
        {
            "s": "CL:0000909",
            "s_label": "CD8-positive, alpha-beta memory T cell",
            "p": "rdfs:subClassOf",
            "o": "CL:0000813",
            "o_label": "memory T cell",
        },
        {
            "s": "CL:0000940",
            "s_label": "mucosal invariant T cell",
            "p": "rdfs:subClassOf",
            "o": "CL:0000842",
            "o_label": "mononuclear cell",
        },
        {
            "s": "CL:0000940",
            "s_label": "mucosal invariant T cell",
            "p": "rdfs:subClassOf",
            "o": "CL:0000789",
            "o_label": "alpha-beta T cell",
        },
        {
            "s": "CL:0000940",
            "s_label": "mucosal invariant T cell",
            "p": "rdfs:subClassOf",
            "o": "CL:0000084",
            "o_label": "T cell",
        },
        {
            "s": "CL:0000980",
            "s_label": "plasmablast",
            "p": "rdfs:subClassOf",
            "o": "CL:0000145",
            "o_label": "professional antigen presenting cell",
        },
        {
            "s": "CL:0000980",
            "s_label": "plasmablast",
            "p": "rdfs:subClassOf",
            "o": "CL:0000236",
            "o_label": "B cell",
        },
        {
            "s": "CL:0000980",
            "s_label": "plasmablast",
            "p": "rdfs:subClassOf",
            "o": "CL:0000842",
            "o_label": "mononuclear cell",
        },
        {
            "s": "CL:0002489",
            "s_label": "double negative thymocyte",
            "p": "rdfs:subClassOf",
            "o": "CL:0000084",
            "o_label": "T cell",
        },
        {
            "s": "CL:0002489",
            "s_label": "double negative thymocyte",
            "p": "rdfs:subClassOf",
            "o": "CL:0000842",
            "o_label": "mononuclear cell",
        },
        {
            "s": "CL:0002489",
            "s_label": "double negative thymocyte",
            "p": "rdfs:subClassOf",
            "o": "CL:0002420",
            "o_label": "immature T cell",
        },
    ]
    expected_minimal_slim_df = pd.DataFrame(
        data_minimal_slim, columns=["s", "s_label", "p", "o", "o_label"]
    ).sort_values("s")

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


def test_full_slim_enrichment():
    data_full_slim = [
        [
            "CL:0000895",
            "naive thymus-derived CD4-positive, alpha-beta T cell",
            "rdfs:subClassOf",
            "CL:0000624",
            "CD4-positive, alpha-beta T cell",
        ],
        [
            "CL:0000897",
            "CD4-positive, alpha-beta memory T cell",
            "rdfs:subClassOf",
            "CL:0000624",
            "CD4-positive, alpha-beta T cell",
        ],
        ["CL:0000980", "plasmablast", "rdfs:subClassOf", "CL:0000236", "B cell"],
        ["CL:0000787", "memory B cell", "rdfs:subClassOf", "CL:0000236", "B cell"],
        ["CL:0000788", "naive B cell", "rdfs:subClassOf", "CL:0000236", "B cell"],
        [
            "CL:0000895",
            "naive thymus-derived CD4-positive, alpha-beta T cell",
            "rdfs:subClassOf",
            "CL:0000624",
            "CD4-positive, alpha-beta T cell",
        ],
        [
            "CL:0000897",
            "CD4-positive, alpha-beta memory T cell",
            "rdfs:subClassOf",
            "CL:0000624",
            "CD4-positive, alpha-beta T cell",
        ],
        ["CL:0000813", "memory T cell", "rdfs:subClassOf", "CL:0000542", "lymphocyte"],
        ["CL:0000815", "regulatory T cell", "rdfs:subClassOf", "CL:0000542", "lymphocyte"],
        ["CL:0000084", "T cell", "rdfs:subClassOf", "CL:0000542", "lymphocyte"],
        ["CL:0000798", "gamma-delta T cell", "rdfs:subClassOf", "CL:0000542", "lymphocyte"],
        ["CL:0000980", "plasmablast", "rdfs:subClassOf", "CL:0000542", "lymphocyte"],
        ["CL:0000940", "mucosal invariant T cell", "rdfs:subClassOf", "CL:0000542", "lymphocyte"],
        ["CL:0000897", "CD4-positive, alpha-beta memory T cell", "rdfs:subClassOf", "CL:0000542", "lymphocyte"],
        ["CL:0000809", "double-positive, alpha-beta thymocyte", "rdfs:subClassOf", "CL:0000542", "lymphocyte"],
        ["CL:0000909", "CD8-positive, alpha-beta memory T cell", "rdfs:subClassOf", "CL:0000542", "lymphocyte"],
        [
            "CL:0000895",
            "naive thymus-derived CD4-positive, alpha-beta T cell",
            "rdfs:subClassOf",
            "CL:0000542",
            "lymphocyte",
        ],
        [
            "CL:0000900",
            "naive thymus-derived CD8-positive, alpha-beta T cell",
            "rdfs:subClassOf",
            "CL:0000542",
            "lymphocyte",
        ],
        ["CL:0002489", "double negative thymocyte", "rdfs:subClassOf", "CL:0000542", "lymphocyte"],
        ["CL:0000787", "memory B cell", "rdfs:subClassOf", "CL:0000542", "lymphocyte"],
        ["CL:0000788", "naive B cell", "rdfs:subClassOf", "CL:0000542", "lymphocyte"],
        ["CL:0000788", "naive B cell", "rdfs:subClassOf", "CL:0000236", "B cell"],
        ["CL:0000980", "plasmablast", "rdfs:subClassOf", "CL:0000236", "B cell"],
        ["CL:0000787", "memory B cell", "rdfs:subClassOf", "CL:0000236", "B cell"],
        [
            "CL:0000895",
            "naive thymus-derived CD4-positive, alpha-beta T cell",
            "rdfs:subClassOf",
            "CL:0000624",
            "CD4-positive, alpha-beta T cell",
        ],
        [
            "CL:0000897",
            "CD4-positive, alpha-beta memory T cell",
            "rdfs:subClassOf",
            "CL:0000624",
            "CD4-positive, alpha-beta T cell",
        ],
        ["CL:0000787", "memory B cell", "rdfs:subClassOf", "CL:0000785", "mature B cell"],
        ["CL:0000788", "naive B cell", "rdfs:subClassOf", "CL:0000785", "mature B cell"],
        ["CL:0000980", "plasmablast", "rdfs:subClassOf", "CL:0000785", "mature B cell"],
        ["CL:0000787", "memory B cell", "rdfs:subClassOf", "CL:0000785", "mature B cell"],
        ["CL:0000788", "naive B cell", "rdfs:subClassOf", "CL:0000785", "mature B cell"],
        ["CL:0000980", "plasmablast", "rdfs:subClassOf", "CL:0000785", "mature B cell"],
        ["CL:0000787", "memory B cell", "rdfs:subClassOf", "CL:0000785", "mature B cell"],
        ["CL:0000788", "naive B cell", "rdfs:subClassOf", "CL:0000785", "mature B cell"],
        ["CL:0000980", "plasmablast", "rdfs:subClassOf", "CL:0000785", "mature B cell"],
        ["CL:0000980", "plasmablast", "rdfs:subClassOf", "CL:0000145", "professional antigen presenting cell"],
        ["CL:0000787", "memory B cell", "rdfs:subClassOf", "CL:0000145", "professional antigen presenting cell"],
        ["CL:0000788", "naive B cell", "rdfs:subClassOf", "CL:0000145", "professional antigen presenting cell"],
        ["CL:0000940", "mucosal invariant T cell", "rdfs:subClassOf", "CL:0000084", "T cell"],
        ["CL:0000897", "CD4-positive, alpha-beta memory T cell", "rdfs:subClassOf", "CL:0000084", "T cell"],
        ["CL:0000798", "gamma-delta T cell", "rdfs:subClassOf", "CL:0000084", "T cell"],
        ["CL:0000813", "memory T cell", "rdfs:subClassOf", "CL:0000084", "T cell"],
        ["CL:0000815", "regulatory T cell", "rdfs:subClassOf", "CL:0000084", "T cell"],
        ["CL:0000809", "double-positive, alpha-beta thymocyte", "rdfs:subClassOf", "CL:0000084", "T cell"],
        [
            "CL:0000900",
            "naive thymus-derived CD8-positive, alpha-beta T cell",
            "rdfs:subClassOf",
            "CL:0000084",
            "T cell",
        ],
        ["CL:0002489", "double negative thymocyte", "rdfs:subClassOf", "CL:0000084", "T cell"],
        ["CL:0000909", "CD8-positive, alpha-beta memory T cell", "rdfs:subClassOf", "CL:0000084", "T cell"],
        [
            "CL:0000895",
            "naive thymus-derived CD4-positive, alpha-beta T cell",
            "rdfs:subClassOf",
            "CL:0000084",
            "T cell",
        ],
        ["CL:0000809", "double-positive, alpha-beta thymocyte", "rdfs:subClassOf", "CL:0000084", "T cell"],
        ["CL:0000940", "mucosal invariant T cell", "rdfs:subClassOf", "CL:0000084", "T cell"],
        ["CL:0000798", "gamma-delta T cell", "rdfs:subClassOf", "CL:0000084", "T cell"],
        ["CL:0000813", "memory T cell", "rdfs:subClassOf", "CL:0000084", "T cell"],
        ["CL:0000815", "regulatory T cell", "rdfs:subClassOf", "CL:0000084", "T cell"],
        [
            "CL:0000895",
            "naive thymus-derived CD4-positive, alpha-beta T cell",
            "rdfs:subClassOf",
            "CL:0000084",
            "T cell",
        ],
        [
            "CL:0000900",
            "naive thymus-derived CD8-positive, alpha-beta T cell",
            "rdfs:subClassOf",
            "CL:0000084",
            "T cell",
        ],
        ["CL:0000897", "CD4-positive, alpha-beta memory T cell", "rdfs:subClassOf", "CL:0000084", "T cell"],
        ["CL:0000909", "CD8-positive, alpha-beta memory T cell", "rdfs:subClassOf", "CL:0000084", "T cell"],
        ["CL:0002489", "double negative thymocyte", "rdfs:subClassOf", "CL:0000084", "T cell"],
        [
            "CL:0000900",
            "naive thymus-derived CD8-positive, alpha-beta T cell",
            "rdfs:subClassOf",
            "CL:0000625",
            "CD8-positive, alpha-beta T cell",
        ],
        [
            "CL:0000909",
            "CD8-positive, alpha-beta memory T cell",
            "rdfs:subClassOf",
            "CL:0000625",
            "CD8-positive, alpha-beta T cell",
        ],
        [
            "CL:0000900",
            "naive thymus-derived CD8-positive, alpha-beta T cell",
            "rdfs:subClassOf",
            "CL:0000625",
            "CD8-positive, alpha-beta T cell",
        ],
        [
            "CL:0000909",
            "CD8-positive, alpha-beta memory T cell",
            "rdfs:subClassOf",
            "CL:0000625",
            "CD8-positive, alpha-beta T cell",
        ],
        [
            "CL:0000900",
            "naive thymus-derived CD8-positive, alpha-beta T cell",
            "rdfs:subClassOf",
            "CL:0000625",
            "CD8-positive, alpha-beta T cell",
        ],
        [
            "CL:0000909",
            "CD8-positive, alpha-beta memory T cell",
            "rdfs:subClassOf",
            "CL:0000625",
            "CD8-positive, alpha-beta T cell",
        ],
        ["CL:0000940", "mucosal invariant T cell", "rdfs:subClassOf", "CL:0002419", "mature T cell"],
        ["CL:0000897", "CD4-positive, alpha-beta memory T cell", "rdfs:subClassOf", "CL:0002419", "mature T cell"],
        ["CL:0000813", "memory T cell", "rdfs:subClassOf", "CL:0002419", "mature T cell"],
        ["CL:0000815", "regulatory T cell", "rdfs:subClassOf", "CL:0002419", "mature T cell"],
        [
            "CL:0000900",
            "naive thymus-derived CD8-positive, alpha-beta T cell",
            "rdfs:subClassOf",
            "CL:0002419",
            "mature T cell",
        ],
        ["CL:0000909", "CD8-positive, alpha-beta memory T cell", "rdfs:subClassOf", "CL:0002419", "mature T cell"],
        [
            "CL:0000895",
            "naive thymus-derived CD4-positive, alpha-beta T cell",
            "rdfs:subClassOf",
            "CL:0002419",
            "mature T cell",
        ],
        ["CL:0000809", "double-positive, alpha-beta thymocyte", "rdfs:subClassOf", "CL:0002420", "immature T cell"],
        ["CL:0002489", "double negative thymocyte", "rdfs:subClassOf", "CL:0002420", "immature T cell"],
        ["CL:0000787", "memory B cell", "rdfs:subClassOf", "CL:0001201", "B cell, CD19-positive"],
        ["CL:0000788", "naive B cell", "rdfs:subClassOf", "CL:0001201", "B cell, CD19-positive"],
        ["CL:0000980", "plasmablast", "rdfs:subClassOf", "CL:0001201", "B cell, CD19-positive"],
        ["CL:0000815", "regulatory T cell", "rdfs:subClassOf", "CL:0002419", "mature T cell"],
        ["CL:0000940", "mucosal invariant T cell", "rdfs:subClassOf", "CL:0002419", "mature T cell"],
        ["CL:0000813", "memory T cell", "rdfs:subClassOf", "CL:0002419", "mature T cell"],
        [
            "CL:0000895",
            "naive thymus-derived CD4-positive, alpha-beta T cell",
            "rdfs:subClassOf",
            "CL:0002419",
            "mature T cell",
        ],
        [
            "CL:0000900",
            "naive thymus-derived CD8-positive, alpha-beta T cell",
            "rdfs:subClassOf",
            "CL:0002419",
            "mature T cell",
        ],
        ["CL:0000897", "CD4-positive, alpha-beta memory T cell", "rdfs:subClassOf", "CL:0002419", "mature T cell"],
        ["CL:0000909", "CD8-positive, alpha-beta memory T cell", "rdfs:subClassOf", "CL:0002419", "mature T cell"],
        ["CL:0000787", "memory B cell", "rdfs:subClassOf", "CL:0001201", "B cell, CD19-positive"],
        ["CL:0000788", "naive B cell", "rdfs:subClassOf", "CL:0001201", "B cell, CD19-positive"],
        ["CL:0000980", "plasmablast", "rdfs:subClassOf", "CL:0001201", "B cell, CD19-positive"],
        ["CL:0000809", "double-positive, alpha-beta thymocyte", "rdfs:subClassOf", "CL:0002420", "immature T cell"],
        ["CL:0002489", "double negative thymocyte", "rdfs:subClassOf", "CL:0002420", "immature T cell"],
        ["CL:0000809", "double-positive, alpha-beta thymocyte", "rdfs:subClassOf", "CL:0000789", "alpha-beta T cell"],
        ["CL:0000940", "mucosal invariant T cell", "rdfs:subClassOf", "CL:0000789", "alpha-beta T cell"],
        [
            "CL:0000895",
            "naive thymus-derived CD4-positive, alpha-beta T cell",
            "rdfs:subClassOf",
            "CL:0000789",
            "alpha-beta T cell",
        ],
        ["CL:0000909", "CD8-positive, alpha-beta memory T cell", "rdfs:subClassOf", "CL:0000789", "alpha-beta T cell"],
        ["CL:0000897", "CD4-positive, alpha-beta memory T cell", "rdfs:subClassOf", "CL:0000789", "alpha-beta T cell"],
        [
            "CL:0000900",
            "naive thymus-derived CD8-positive, alpha-beta T cell",
            "rdfs:subClassOf",
            "CL:0000789",
            "alpha-beta T cell",
        ],
        ["CL:0000809", "double-positive, alpha-beta thymocyte", "rdfs:subClassOf", "CL:0000789", "alpha-beta T cell"],
        ["CL:0000940", "mucosal invariant T cell", "rdfs:subClassOf", "CL:0000789", "alpha-beta T cell"],
        [
            "CL:0000895",
            "naive thymus-derived CD4-positive, alpha-beta T cell",
            "rdfs:subClassOf",
            "CL:0000789",
            "alpha-beta T cell",
        ],
        ["CL:0000909", "CD8-positive, alpha-beta memory T cell", "rdfs:subClassOf", "CL:0000789", "alpha-beta T cell"],
        ["CL:0000897", "CD4-positive, alpha-beta memory T cell", "rdfs:subClassOf", "CL:0000789", "alpha-beta T cell"],
        [
            "CL:0000900",
            "naive thymus-derived CD8-positive, alpha-beta T cell",
            "rdfs:subClassOf",
            "CL:0000789",
            "alpha-beta T cell",
        ],
        [
            "CL:0000897",
            "CD4-positive, alpha-beta memory T cell",
            "rdfs:subClassOf",
            "CL:0000791",
            "mature alpha-beta T cell",
        ],
        [
            "CL:0000900",
            "naive thymus-derived CD8-positive, alpha-beta T cell",
            "rdfs:subClassOf",
            "CL:0000791",
            "mature alpha-beta T cell",
        ],
        [
            "CL:0000909",
            "CD8-positive, alpha-beta memory T cell",
            "rdfs:subClassOf",
            "CL:0000791",
            "mature alpha-beta T cell",
        ],
        ["CL:0000940", "mucosal invariant T cell", "rdfs:subClassOf", "CL:0000791", "mature alpha-beta T cell"],
        [
            "CL:0000895",
            "naive thymus-derived CD4-positive, alpha-beta T cell",
            "rdfs:subClassOf",
            "CL:0000791",
            "mature alpha-beta T cell",
        ],
        ["CL:0000809", "double-positive, alpha-beta thymocyte", "rdfs:subClassOf", "CL:0000789", "alpha-beta T cell"],
        ["CL:0000940", "mucosal invariant T cell", "rdfs:subClassOf", "CL:0000789", "alpha-beta T cell"],
        [
            "CL:0000895",
            "naive thymus-derived CD4-positive, alpha-beta T cell",
            "rdfs:subClassOf",
            "CL:0000789",
            "alpha-beta T cell",
        ],
        ["CL:0000909", "CD8-positive, alpha-beta memory T cell", "rdfs:subClassOf", "CL:0000789", "alpha-beta T cell"],
        ["CL:0000897", "CD4-positive, alpha-beta memory T cell", "rdfs:subClassOf", "CL:0000789", "alpha-beta T cell"],
        [
            "CL:0000900",
            "naive thymus-derived CD8-positive, alpha-beta T cell",
            "rdfs:subClassOf",
            "CL:0000789",
            "alpha-beta T cell",
        ],
        ["CL:0000809", "double-positive, alpha-beta thymocyte", "rdfs:subClassOf", "CL:0002420", "immature T cell"],
        ["CL:0002489", "double negative thymocyte", "rdfs:subClassOf", "CL:0002420", "immature T cell"],
        [
            "CL:0000900",
            "naive thymus-derived CD8-positive, alpha-beta T cell",
            "rdfs:subClassOf",
            "CL:0000791",
            "mature alpha-beta T cell",
        ],
        [
            "CL:0000909",
            "CD8-positive, alpha-beta memory T cell",
            "rdfs:subClassOf",
            "CL:0000791",
            "mature alpha-beta T cell",
        ],
        ["CL:0000940", "mucosal invariant T cell", "rdfs:subClassOf", "CL:0000791", "mature alpha-beta T cell"],
        [
            "CL:0000895",
            "naive thymus-derived CD4-positive, alpha-beta T cell",
            "rdfs:subClassOf",
            "CL:0000791",
            "mature alpha-beta T cell",
        ],
        [
            "CL:0000897",
            "CD4-positive, alpha-beta memory T cell",
            "rdfs:subClassOf",
            "CL:0000791",
            "mature alpha-beta T cell",
        ],
        [
            "CL:0000809",
            "double-positive, alpha-beta thymocyte",
            "rdfs:subClassOf",
            "CL:0000790",
            "immature alpha-beta T cell",
        ],
        [
            "CL:0000809",
            "double-positive, alpha-beta thymocyte",
            "rdfs:subClassOf",
            "CL:0000790",
            "immature alpha-beta T cell",
        ],
        [
            "CL:0000897",
            "CD4-positive, alpha-beta memory T cell",
            "rdfs:subClassOf",
            "CL:0000791",
            "mature alpha-beta T cell",
        ],
        [
            "CL:0000900",
            "naive thymus-derived CD8-positive, alpha-beta T cell",
            "rdfs:subClassOf",
            "CL:0000791",
            "mature alpha-beta T cell",
        ],
        [
            "CL:0000909",
            "CD8-positive, alpha-beta memory T cell",
            "rdfs:subClassOf",
            "CL:0000791",
            "mature alpha-beta T cell",
        ],
        ["CL:0000940", "mucosal invariant T cell", "rdfs:subClassOf", "CL:0000791", "mature alpha-beta T cell"],
        [
            "CL:0000895",
            "naive thymus-derived CD4-positive, alpha-beta T cell",
            "rdfs:subClassOf",
            "CL:0000791",
            "mature alpha-beta T cell",
        ],
        [
            "CL:0000809",
            "double-positive, alpha-beta thymocyte",
            "rdfs:subClassOf",
            "CL:0000790",
            "immature alpha-beta T cell",
        ],
        [
            "CL:0000809",
            "double-positive, alpha-beta thymocyte",
            "rdfs:subClassOf",
            "CL:0000790",
            "immature alpha-beta T cell",
        ],
        ["CL:0000897", "CD4-positive, alpha-beta memory T cell", "rdfs:subClassOf", "CL:0000813", "memory T cell"],
        ["CL:0000909", "CD8-positive, alpha-beta memory T cell", "rdfs:subClassOf", "CL:0000813", "memory T cell"],
        ["CL:0000809", "double-positive, alpha-beta thymocyte", "rdfs:subClassOf", "CL:0000893", "thymocyte"],
        ["CL:0002489", "double negative thymocyte", "rdfs:subClassOf", "CL:0000893", "thymocyte"],
        ["CL:0000897", "CD4-positive, alpha-beta memory T cell", "rdfs:subClassOf", "CL:0000813", "memory T cell"],
        ["CL:0000909", "CD8-positive, alpha-beta memory T cell", "rdfs:subClassOf", "CL:0000813", "memory T cell"],
        ["CL:0000897", "CD4-positive, alpha-beta memory T cell", "rdfs:subClassOf", "CL:0000813", "memory T cell"],
        ["CL:0000909", "CD8-positive, alpha-beta memory T cell", "rdfs:subClassOf", "CL:0000813", "memory T cell"],
        ["CL:0000084", "T cell", "rdfs:subClassOf", "CL:0000842", "mononuclear cell"],
        ["CL:0000798", "gamma-delta T cell", "rdfs:subClassOf", "CL:0000842", "mononuclear cell"],
        ["CL:0000813", "memory T cell", "rdfs:subClassOf", "CL:0000842", "mononuclear cell"],
        ["CL:0000815", "regulatory T cell", "rdfs:subClassOf", "CL:0000842", "mononuclear cell"],
        ["CL:0000980", "plasmablast", "rdfs:subClassOf", "CL:0000842", "mononuclear cell"],
        ["CL:0000809", "double-positive, alpha-beta thymocyte", "rdfs:subClassOf", "CL:0000842", "mononuclear cell"],
        ["CL:0000940", "mucosal invariant T cell", "rdfs:subClassOf", "CL:0000842", "mononuclear cell"],
        [
            "CL:0000895",
            "naive thymus-derived CD4-positive, alpha-beta T cell",
            "rdfs:subClassOf",
            "CL:0000842",
            "mononuclear cell",
        ],
        [
            "CL:0000900",
            "naive thymus-derived CD8-positive, alpha-beta T cell",
            "rdfs:subClassOf",
            "CL:0000842",
            "mononuclear cell",
        ],
        ["CL:0000897", "CD4-positive, alpha-beta memory T cell", "rdfs:subClassOf", "CL:0000842", "mononuclear cell"],
        ["CL:0000909", "CD8-positive, alpha-beta memory T cell", "rdfs:subClassOf", "CL:0000842", "mononuclear cell"],
        ["CL:0002489", "double negative thymocyte", "rdfs:subClassOf", "CL:0000842", "mononuclear cell"],
        ["CL:0000787", "memory B cell", "rdfs:subClassOf", "CL:0000842", "mononuclear cell"],
        ["CL:0000788", "naive B cell", "rdfs:subClassOf", "CL:0000842", "mononuclear cell"],
        ["CL:0000809", "double-positive, alpha-beta thymocyte", "rdfs:subClassOf", "CL:0000893", "thymocyte"],
        ["CL:0002489", "double negative thymocyte", "rdfs:subClassOf", "CL:0000893", "thymocyte"],
        [
            "CL:0000895",
            "naive thymus-derived CD4-positive, alpha-beta T cell",
            "rdfs:subClassOf",
            "CL:0000898",
            "naive T cell",
        ],
        [
            "CL:0000900",
            "naive thymus-derived CD8-positive, alpha-beta T cell",
            "rdfs:subClassOf",
            "CL:0000898",
            "naive T cell",
        ],
        ["CL:0000809", "double-positive, alpha-beta thymocyte", "rdfs:subClassOf", "CL:0000893", "thymocyte"],
        ["CL:0002489", "double negative thymocyte", "rdfs:subClassOf", "CL:0000893", "thymocyte"],
        [
            "CL:0000900",
            "naive thymus-derived CD8-positive, alpha-beta T cell",
            "rdfs:subClassOf",
            "CL:0000898",
            "naive T cell",
        ],
        [
            "CL:0000895",
            "naive thymus-derived CD4-positive, alpha-beta T cell",
            "rdfs:subClassOf",
            "CL:0000898",
            "naive T cell",
        ],
        ["CL:0000980", "plasmablast", "rdfs:subClassOf", "CL:0000945", "lymphocyte of B lineage"],
        ["CL:0000788", "naive B cell", "rdfs:subClassOf", "CL:0000945", "lymphocyte of B lineage"],
        ["CL:0000787", "memory B cell", "rdfs:subClassOf", "CL:0000945", "lymphocyte of B lineage"],
        ["CL:0000787", "memory B cell", "rdfs:subClassOf", "CL:0001200", "lymphocyte of B lineage, CD19-positive"],
        ["CL:0000788", "naive B cell", "rdfs:subClassOf", "CL:0001200", "lymphocyte of B lineage, CD19-positive"],
        ["CL:0000980", "plasmablast", "rdfs:subClassOf", "CL:0001200", "lymphocyte of B lineage, CD19-positive"],
        ["CL:0000980", "plasmablast", "rdfs:subClassOf", "CL:0000946", "antibody secreting cell"],
    ]

    expected_full_slim_df = pd.DataFrame(data_full_slim, columns=["s", "s_label", "p", "o", "o_label"]).sort_values("s")

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


def test_contextual_slim_enrichment():
    data_contextual = [
        {
            "s": "CL:1000597",
            "s_label": "papillary tips cell",
            "p": "rdfs:subClassOf",
            "o": "CL:1000504",
            "o_label": "kidney medulla cell",
        },
        {
            "s": "CL:1000597",
            "s_label": "papillary tips cell",
            "p": "rdfs:subClassOf",
            "o": "CL:1000617",
            "o_label": "kidney inner medulla cell",
        },
        {
            "s": "CL:1001107",
            "s_label": "kidney loop of Henle thin ascending limb epithelial cell",
            "p": "rdfs:subClassOf",
            "o": "CL:1000504",
            "o_label": "kidney medulla cell",
        },
        {
            "s": "CL:1001108",
            "s_label": "kidney loop of Henle medullary thick ascending limb epithelial cell",
            "p": "rdfs:subClassOf",
            "o": "CL:1000504",
            "o_label": "kidney medulla cell",
        },
        {
            "s": "CL:1001111",
            "s_label": "kidney loop of Henle thin descending limb epithelial cell",
            "p": "rdfs:subClassOf",
            "o": "CL:1000504",
            "o_label": "kidney medulla cell",
        },
        {
            "s": "CL:1001108",
            "s_label": "kidney loop of Henle medullary thick ascending limb epithelial cell",
            "p": "rdfs:subClassOf",
            "o": "CL:1000616",
            "o_label": "kidney outer medulla cell",
        },
        {
            "s": "CL:1001111",
            "s_label": "kidney loop of Henle thin descending limb epithelial cell",
            "p": "rdfs:subClassOf",
            "o": "CL:1000616",
            "o_label": "kidney outer medulla cell",
        },
        {
            "s": "CL:1001107",
            "s_label": "kidney loop of Henle thin ascending limb epithelial cell",
            "p": "rdfs:subClassOf",
            "o": "CL:1000617",
            "o_label": "kidney inner medulla cell",
        },
        {
            "s": "CL:1001108",
            "s_label": "kidney loop of Henle medullary thick ascending limb epithelial cell",
            "p": "rdfs:subClassOf",
            "o": "CL:1001106",
            "o_label": "kidney loop of Henle thick ascending limb epithelial cell",
        },
    ]
    expected_contextual_df = pd.DataFrame(data_contextual, columns=["s", "s_label", "p", "o", "o_label"]).sort_values(
        "s"
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


# def test_synonym_lookup_empty_df():
#     q = Query(kidney_test_data)
#
#     with pytest.raises(EnrichedDataFrameEmpty) as exc_info:
#         q.synonym_lookup()
#
#     expected_message = (
#         "The enriched DataFrame cannot be empty for synonym lookup. Please use an enrichment method first"
#     )
#     assert str(exc_info.value) == expected_message


def test_synonym_lookup(mocker):
    q = Query(
        [
            "CL:0000084",
            "CL:0000813",
            "CL:0000815",
            "CL:0000900",
        ]
    )

    # Mock the run_sparql_query function in query
    mocker.patch(
        "pandasaurus.query.run_sparql_query",
        side_effect=[
            iter(
                [
                    {
                        "o": "CL:0000084",
                        "s": "CL:0000813",
                        "p": "rdfs:subClassOf",
                        "s_label": "memory T cell",
                        "o_label": "T cell",
                    },
                    {
                        "o": "CL:0000084",
                        "s": "CL:0000815",
                        "p": "rdfs:subClassOf",
                        "s_label": "regulatory T cell",
                        "o_label": "T cell",
                    },
                    {
                        "o": "CL:0000084",
                        "s": "CL:0000900",
                        "p": "rdfs:subClassOf",
                        "s_label": "naive thymus-derived CD8-positive, alpha-beta T cell",
                        "o_label": "T cell",
                    },
                ]
            ),
            iter(
                [
                    {"s": "CL:0000084"},
                    {"s": "CL:0000813"},
                    {"s": "CL:0000815"},
                    {"s": "CL:0000900", "narrow_synonym": "T.8Nve.Sp"},
                    {"s": "CL:0000084", "exact_synonym": "T lymphocyte"},
                    {"s": "CL:0000084", "exact_synonym": "T-cell"},
                    {"s": "CL:0000084", "exact_synonym": "T-lymphocyte"},
                    {"s": "CL:0000813", "exact_synonym": "memory T lymphocyte"},
                    {"s": "CL:0000813", "exact_synonym": "memory T-cell"},
                    {"s": "CL:0000813", "exact_synonym": "memory T-lymphocyte"},
                    {"s": "CL:0000815", "exact_synonym": "regulatory T lymphocyte"},
                    {"s": "CL:0000815", "exact_synonym": "regulatory T-cell"},
                    {"s": "CL:0000815", "exact_synonym": "regulatory T-lymphocyte"},
                    {"s": "CL:0000815", "exact_synonym": "Treg"},
                    {"s": "CL:0000900", "exact_synonym": "naive thymus-dervied CD8-positive, alpha-beta T lymphocyte"},
                    {"s": "CL:0000900", "exact_synonym": "naive thymus-dervied CD8-positive, alpha-beta T-cell"},
                    {"s": "CL:0000900", "exact_synonym": "naive thymus-dervied CD8-positive, alpha-beta T-lymphocyte"},
                    {"s": "CL:0000084", "related_synonym": "immature T cell"},
                    {"s": "CL:0000084", "related_synonym": "mature T cell"},
                    {"s": "CL:0000813"},
                    {"s": "CL:0000815"},
                    {"s": "CL:0000900"},
                    {"s": "CL:0000084"},
                    {"s": "CL:0000813"},
                    {"s": "CL:0000815", "broad_synonym": "suppressor T cell"},
                    {"s": "CL:0000815", "broad_synonym": "suppressor T lymphocyte"},
                    {"s": "CL:0000815", "broad_synonym": "suppressor T-cell"},
                    {"s": "CL:0000815", "broad_synonym": "suppressor T-lymphocyte"},
                    {"s": "CL:0000900", "broad_synonym": "naive CD8+ T cell"},
                ]
            ),
        ],
    )

    q.simple_enrichment()
    result_df = q.synonym_lookup()

    expected_df = pd.DataFrame(
        [
            {"ID": "CL:0000084", "label": "T cell", "name": "T lymphocyte", "type": "exact_synonym"},
            {"ID": "CL:0000084", "label": "T cell", "name": "T-cell", "type": "exact_synonym"},
            {"ID": "CL:0000084", "label": "T cell", "name": "T-lymphocyte", "type": "exact_synonym"},
            {"ID": "CL:0000084", "label": "T cell", "name": "immature T cell", "type": "related_synonym"},
            {"ID": "CL:0000084", "label": "T cell", "name": "mature T cell", "type": "related_synonym"},
            {"ID": "CL:0000813", "label": "memory T cell", "name": "memory T lymphocyte", "type": "exact_synonym"},
            {"ID": "CL:0000813", "label": "memory T cell", "name": "memory T-cell", "type": "exact_synonym"},
            {"ID": "CL:0000813", "label": "memory T cell", "name": "memory T-lymphocyte", "type": "exact_synonym"},
            {"ID": "CL:0000815", "label": "regulatory T cell", "name": "Treg", "type": "exact_synonym"},
            {
                "ID": "CL:0000815",
                "label": "regulatory T cell",
                "name": "regulatory T lymphocyte",
                "type": "exact_synonym",
            },
            {"ID": "CL:0000815", "label": "regulatory T cell", "name": "regulatory T-cell", "type": "exact_synonym"},
            {
                "ID": "CL:0000815",
                "label": "regulatory T cell",
                "name": "regulatory T-lymphocyte",
                "type": "exact_synonym",
            },
            {
                "ID": "CL:0000815",
                "label": "regulatory T cell",
                "name": "suppressor T-lymphocyte",
                "type": "broad_synonym",
            },
            {"ID": "CL:0000815", "label": "regulatory T cell", "name": "suppressor T-cell", "type": "broad_synonym"},
            {
                "ID": "CL:0000815",
                "label": "regulatory T cell",
                "name": "suppressor T lymphocyte",
                "type": "broad_synonym",
            },
            {"ID": "CL:0000815", "label": "regulatory T cell", "name": "suppressor T cell", "type": "broad_synonym"},
            {
                "ID": "CL:0000900",
                "label": "naive thymus-derived CD8-positive, alpha-beta T cell",
                "name": "T.8Nve.Sp",
                "type": "narrow_synonym",
            },
            {
                "ID": "CL:0000900",
                "label": "naive thymus-derived CD8-positive, alpha-beta T cell",
                "name": "naive thymus-dervied CD8-positive, alpha-beta T-cell",
                "type": "exact_synonym",
            },
            {
                "ID": "CL:0000900",
                "label": "naive thymus-derived CD8-positive, alpha-beta T cell",
                "name": "naive thymus-dervied CD8-positive, alpha-beta T lymphocyte",
                "type": "exact_synonym",
            },
            {
                "ID": "CL:0000900",
                "label": "naive thymus-derived CD8-positive, alpha-beta T cell",
                "name": "naive thymus-dervied CD8-positive, alpha-beta T-lymphocyte",
                "type": "exact_synonym",
            },
            {
                "ID": "CL:0000900",
                "label": "naive thymus-derived CD8-positive, alpha-beta T cell",
                "name": "naive CD8+ T cell",
                "type": "broad_synonym",
            },
        ]
    )

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
