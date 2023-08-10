from test.data.graph_generator_data import (
    get_generate_enrichment_graph_data,
    get_nonredundant_expected_triples,
    get_redundant_expected_triples,
)

import pandas as pd

from pandasaurus.graph.graph_generator import GraphGenerator


def test_generate_enrichment_graph():
    graph = GraphGenerator.generate_enrichment_graph(pd.DataFrame(get_generate_enrichment_graph_data()))
    expected_triples = get_redundant_expected_triples()
    for triple in graph:
        assert triple in expected_triples


def test_apply_transitive_reduction():
    test_df = pd.DataFrame(get_generate_enrichment_graph_data())
    graph = GraphGenerator.generate_enrichment_graph(test_df)
    graph = GraphGenerator.apply_transitive_reduction(graph, test_df["p"].unique().tolist())
    expected_triples = get_nonredundant_expected_triples()
    for triple in graph:
        assert triple in expected_triples
