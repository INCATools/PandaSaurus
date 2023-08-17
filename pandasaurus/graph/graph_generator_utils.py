from rdflib import Graph


def add_edge(nx_graph, subject, predicate, obj):
    edge_data = {"label": str(predicate).split("#")[-1] if "#" in predicate else str(predicate).split("/")[-1]}
    nx_graph.add_edge(
        str(subject),
        str(obj),
        **edge_data,
    )


def add_outgoing_edges_to_subgraph(graph, predicate_uri=None):
    """
    Add all outgoing edges of a node in the graph to the subgraph.

    Parameters:
        graph (Graph): The RDF graph containing the triples.
        predicate_uri (URIRef or None): The predicate to filter triples (optional).

    Returns:
        rdflib.Graph: The subgraph containing the outgoing edges of the nodes.
    """
    subgraph = Graph()
    for s, p, o in graph.triples((None, predicate_uri, None)):
        subgraph.add((s, p, o))

    return subgraph
