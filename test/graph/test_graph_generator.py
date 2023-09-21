import logging
from test.data.graph_generator_data import (
    get_generate_enrichment_graph_data,
    get_nonredundant_expected_triples,
    get_redundant_expected_triples,
)

import pandas as pd
import pytest

from pandasaurus.graph.graph_generator import GraphGenerator
from pandasaurus.utils.logging_config import configure_logger

logger = configure_logger()


@pytest.fixture
def sample_test_df():
    return pd.DataFrame(get_generate_enrichment_graph_data())


@pytest.fixture
def sample_rdf_graph(sample_test_df):
    return GraphGenerator.generate_enrichment_graph(sample_test_df)


def test_generate_enrichment_graph(sample_rdf_graph):
    expected_triples = get_redundant_expected_triples()
    for triple in sample_rdf_graph:
        assert triple in expected_triples


def test_apply_transitive_reduction(sample_test_df, sample_rdf_graph):
    graph = GraphGenerator.apply_transitive_reduction(sample_rdf_graph, sample_test_df["p"].unique().tolist())
    expected_triples = get_nonredundant_expected_triples()
    for triple in graph:
        assert triple in expected_triples


def test_apply_transitive_reduction_with_invalid_predicates(sample_test_df, sample_rdf_graph, caplog):
    caplog.set_level(logging.ERROR, logger="pandasaurus.utils.logging_config")
    # Configure caplog to capture log messages from your logger
    # caplog.set_level(logging.DEBUG, logger="__name__")  # Replace "__name__" with your logger's name

    # Perform some actions that generate log messages
    invalid_predicate_list = ["invalid_predicate"]
    GraphGenerator.apply_transitive_reduction(sample_rdf_graph, invalid_predicate_list)
    assert "The predicate 'invalid_predicate' does not exist in the graph" in caplog.text

    # expected_triples = get_nonredundant_expected_triples()
    # for triple in graph:
    #     assert triple in expected_triples
