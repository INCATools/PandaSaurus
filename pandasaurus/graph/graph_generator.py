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
        invalid_predicates = []
        # TODO We need a better way to handle the queries, and decide the format we accept in the predicate list
        ask_query = prepareQuery(f"ASK {{ ?s ?p ?o }}")
        for predicate in predicate_list:
            if predicate and not graph.query(ask_query, initNs={"rdfs": RDFS}):
                invalid_predicates.append(predicate)
                continue

            predicate_ = RDFS.subClassOf if predicate == "rdfs:subClassOf" else URIRef(predicate)
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
                # if graph.query(f"ASK {{ <{edge[0]}> <{predicate}> <{edge[1]}> }}"):
                graph.remove((URIRef(edge[0]), predicate_, URIRef(edge[1])))
            logger.info(f"Transitive reduction has been applied on {predicate}.")

        if invalid_predicates:
            error_msg = (
                f"The predicate '{invalid_predicates[0]}' does not exist in the graph"
                if len(invalid_predicates) == 1
                else f"The predicates {' ,'.join(invalid_predicates)} do not exist in the graph"
            )
            logger.error(error_msg)

        return graph