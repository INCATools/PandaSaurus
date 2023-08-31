from typing import List

import networkx as nx
import pandas as pd
from rdflib import RDF, RDFS, Graph, Literal, Namespace, URIRef
from rdflib.plugins.sparql import prepareQuery

from pandasaurus.graph.graph_generator_utils import (
    add_edge,
    add_outgoing_edges_to_subgraph,
)
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
            graph.add((o, RDFS.label, Literal(row["o_label"])))
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
        # TODO We need a better way to handle the queries, and decide the format we accept in the predicate list
        ask_query = prepareQuery("SELECT ?s ?p WHERE { ?s ?p ?o }")
        for predicate in predicate_list:
            predicate_ = RDFS.subClassOf if predicate == "rdfs:subClassOf" else URIRef(predicate)
            if predicate and not graph.query(ask_query, initBindings={"p": predicate_}, initNs={"rdfs": RDFS}):
                invalid_predicates.append(predicate)
                continue

            subgraph = add_outgoing_edges_to_subgraph(graph, predicate_)

            nx_graph = nx.DiGraph()
            for s, p, o in subgraph:
                if isinstance(o, URIRef) and p != RDF.type:
                    add_edge(nx_graph, s, predicate, o)

            # Apply transitive reduction to remove redundancy
            transitive_reduction_graph = nx.transitive_reduction(nx_graph)
            transitive_reduction_graph.add_edges_from(
                (u, v, nx_graph.edges[u, v]) for u, v in transitive_reduction_graph.edges
            )
            # Remove redundant triples using nx graph
            edge_diff = list(set(nx_graph.edges) - set(transitive_reduction_graph.edges))
            for edge in edge_diff:
                graph.remove((URIRef(edge[0]), predicate_, URIRef(edge[1])))
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
