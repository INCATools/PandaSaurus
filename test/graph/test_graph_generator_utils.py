import networkx as nx
from rdflib import Graph, URIRef

from pandasaurus.graph.graph_generator_utils import (
    add_edge,
    add_outgoing_edges_to_subgraph,
)


def test_add_edge_with_hashtag():
    nx_graph = nx.DiGraph()
    subject = "http://example.org/subject"
    predicate = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
    obj = "http://example.org/object"

    add_edge(nx_graph, subject, predicate, obj)

    assert nx_graph.has_edge(subject, obj)
    assert nx_graph.get_edge_data(subject, obj)["label"] == "type"


def test_add_edge_without_hashtag():
    nx_graph = nx.DiGraph()
    subject = "http://example.org/subject"
    predicate = "http://example.org/consist_of"
    obj = "http://example.org/object"

    add_edge(nx_graph, subject, predicate, obj)

    assert nx_graph.has_edge(subject, obj)
    assert nx_graph.get_edge_data(subject, obj)["label"] == "consist_of"


def test_add_outgoing_edges_to_subgraph_with_predicate():
    graph = Graph()
    graph.add(
        (
            URIRef("http://example.org/subject"),
            URIRef("http://example.org/predicate"),
            URIRef("http://example.org/object"),
        )
    )
    graph.add(
        (
            URIRef("http://example.org/subject"),
            URIRef("http://example.org/other_predicate"),
            URIRef("http://example.org/other_object"),
        )
    )

    predicate_uri = URIRef("http://example.org/predicate")
    subgraph = add_outgoing_edges_to_subgraph(graph, predicate_uri)

    assert len(subgraph) == 1
    assert (
        URIRef("http://example.org/subject"),
        URIRef("http://example.org/predicate"),
        URIRef("http://example.org/object"),
    ) in subgraph


def test_add_outgoing_edges_to_subgraph_without_predicate():
    graph = Graph()
    graph.add(
        (
            URIRef("http://example.org/subject"),
            URIRef("http://example.org/predicate"),
            URIRef("http://example.org/object"),
        )
    )
    graph.add(
        (
            URIRef("http://example.org/subject"),
            URIRef("http://example.org/other_predicate"),
            URIRef("http://example.org/other_object"),
        )
    )

    subgraph = add_outgoing_edges_to_subgraph(graph)

    assert len(subgraph) == 2
    assert (
        URIRef("http://example.org/subject"),
        URIRef("http://example.org/predicate"),
        URIRef("http://example.org/object"),
    ) in subgraph
    assert (
        URIRef("http://example.org/subject"),
        URIRef("http://example.org/other_predicate"),
        URIRef("http://example.org/other_object"),
    ) in subgraph
