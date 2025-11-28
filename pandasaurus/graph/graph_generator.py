from typing import List

import networkx as nx
import pandas as pd
from rdflib import OWL, RDF, RDFS, Graph, Literal, Namespace, URIRef
from rdflib.plugins.sparql import prepareQuery

from pandasaurus.utils.logging_config import configure_logger

# Set up logger
logger = configure_logger()


class GraphGenerator:
    @staticmethod
    def generate_enrichment_graph(enriched_df: pd.DataFrame) -> Graph:
        """
        Generates an RDF graph representing enrichment relationships from an enriched DataFrame.

        Args:
            enriched_df (pd.DataFrame): A DataFrame containing enrichment relationships.
                It should have columns 's', 's_label', 'o', and 'o_label' representing subjects,
                subject labels, objects, and object labels respectively.

        Returns:
            Graph: An RDF graph representing the enrichment relationships.
                Each subject is linked to its corresponding object using the 'subClassOf' relationship,
                and labels are associated with subjects and objects using the 'label' relationship.
        """
        graph = Graph()
        cl_namespace = Namespace("http://purl.obolibrary.org/obo/CL_")
        for _, row in enriched_df.iterrows():
            s = cl_namespace[row["s"].split(":")[-1]]
            o = cl_namespace[row["o"].split(":")[-1]]
            graph.add((s, RDFS.label, Literal(row["s_label"])))
            graph.add((s, RDF.type, OWL.Class))
            graph.add((o, RDFS.label, Literal(row["o_label"])))
            graph.add((o, RDF.type, OWL.Class))
            graph.add((s, RDFS.subClassOf, o))
        return graph

    @staticmethod
    def apply_transitive_reduction(graph: Graph, predicate_list: List[str]) -> Graph:
        """
        Applies transitive reduction to a given RDF graph using specified predicates.

        Args:
            graph (Graph): The RDF graph to which transitive reduction is applied.
            predicate_list (List[str]): A list of predicates (URIs or 'rdfs:subClassOf')
                to which transitive reduction will be applied.

        Returns:
            Graph: The RDF graph after applying transitive reduction to the specified predicates.

        Note:
            - The method applies transitive reduction to the specified predicates by adding only the necessary edges
              to create a directed acyclic graph.
            - Redundant triples are removed from the graph using transitive reduction results.
            - The 'predicate_list' should contain valid predicates existing in the graph.
            - For 'predicate_list', you can use either full URIs or 'rdfs:subClassOf' for the RDF schema 'subClassOf'
              relationship.
        """
        invalid_predicates = []
        for predicate in predicate_list:
            predicate_uri = GraphGenerator._normalize_predicate(predicate)
            if not GraphGenerator._predicate_exists(graph, predicate_uri):
                invalid_predicates.append(predicate)
                continue

            subgraph = GraphGenerator._add_outgoing_edges_to_subgraph(graph, predicate_uri)
            nx_graph = GraphGenerator._build_networkx_graph(subgraph, predicate)
            redundant_edges = GraphGenerator._compute_redundant_edges(nx_graph)
            GraphGenerator._remove_redundant_triples(graph, redundant_edges, predicate_uri)
            # TODO Temporarily disabling this log message
            # logger.info(f"Transitive reduction has been applied on {predicate} for graph generation.")

        if invalid_predicates:
            error_msg = (
                f"The predicate '{invalid_predicates[0]}' does not exist in the graph"
                if len(invalid_predicates) == 1
                else f"The predicates {' ,'.join(invalid_predicates)} do not exist in the graph"
            )
            logger.error(error_msg)

        return graph

    @staticmethod
    def _normalize_predicate(predicate: str) -> URIRef:
        """Return the RDF predicate URI, handling the rdfs:subClassOf shortcut."""
        return RDFS.subClassOf if predicate == "rdfs:subClassOf" else URIRef(predicate)

    @staticmethod
    def _predicate_exists(graph: Graph, predicate_uri: URIRef) -> bool:
        """Check whether the predicate occurs in the graph before processing."""
        ask_query = prepareQuery("SELECT ?s ?p WHERE { ?s ?p ?o }")
        return bool(graph.query(ask_query, initBindings={"p": predicate_uri}, initNs={"rdfs": RDFS}))

    @staticmethod
    def _build_networkx_graph(subgraph: Graph, predicate: str) -> nx.DiGraph:
        """Convert the rdflib subgraph into a networkx DiGraph for reduction."""
        nx_graph = nx.DiGraph()
        for s, p, o in subgraph:
            if isinstance(o, URIRef) and p != RDF.type:
                GraphGenerator._add_edge(nx_graph, s, predicate, o)
        return nx_graph

    @staticmethod
    def _compute_redundant_edges(nx_graph: nx.DiGraph) -> List[tuple]:
        """Return the edges that should be removed after a transitive reduction."""
        transitive_reduction_graph = nx.transitive_reduction(nx_graph)
        transitive_reduction_graph.add_edges_from(
            (u, v, nx_graph.edges[u, v]) for u, v in transitive_reduction_graph.edges
        )
        return list(set(nx_graph.edges) - set(transitive_reduction_graph.edges))

    @staticmethod
    def _remove_redundant_triples(graph: Graph, redundant_edges: List[tuple], predicate_uri: URIRef) -> None:
        """Remove redundant triples from the rdflib graph using the computed edge list."""
        for source, target in redundant_edges:
            graph.remove((URIRef(source), predicate_uri, URIRef(target)))

    @staticmethod
    def _add_edge(nx_graph, subject, predicate, obj):
        edge_data = {"label": str(predicate).split("#")[-1] if "#" in predicate else str(predicate).split("/")[-1]}
        nx_graph.add_edge(
            str(subject),
            str(obj),
            **edge_data,
        )

    @staticmethod
    def _add_outgoing_edges_to_subgraph(graph, predicate_uri=None):
        subgraph = Graph()
        for s, p, o in graph.triples((None, predicate_uri, None)):
            subgraph.add((s, p, o))

        return subgraph
