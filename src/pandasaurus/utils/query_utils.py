from typing import List

from sparql_queries import (
    get_contextual_enrichment_query,
    get_curie_prefix_validation_query,
    get_curie_validation_query,
    get_full_enrichment_query,
    get_minimal_enrichment_query,
    get_obsolete_term_query,
    get_replaced_by_query,
    get_simple_enrichment_query,
    get_slim_details_query,
    get_slim_list_query,
)
from SPARQLWrapper import JSON, SPARQLWrapper

from ..config import default_config

# SPARQLWrapper init
sparql = SPARQLWrapper(default_config["UBERGRAPH_ENDPOINT"])
sparql.setReturnFormat(JSON)


def retrieve_simple_slim_triples(seed_list: List[str]):
    # TODO Add missing implementation
    pass


def retrieve_minimal_slim_triples(seed_list: List[str]):
    # TODO Add missing implementation
    pass


def retrieve_full_slim_triples(seed_list: List[str]):
    # TODO Add missing implementation
    pass


def retrieve_contextual_slim_triples(seed_list: List[str]):
    # TODO Add missing implementation
    pass


def run_curie_prefix_query(curie_list: List[str]):
    sparql.setQuery(get_curie_prefix_validation_query(curie_list))
    # TODO Add missing implementation
    pass


def run_curie_list_query(curie_list: List[str]):
    sparql.setQuery(get_curie_validation_query(curie_list))
    # TODO Add missing implementation
    pass


def run_obsolete_term_query(curie_list: List[str]):
    sparql.setQuery(get_obsolete_term_query(curie_list))
    # TODO Add missing implementation
    pass


def run_replaced_by_query(curie_list: List[str]):
    sparql.setQuery(get_replaced_by_query(curie_list))
    # TODO Add missing implementation
    pass


def run_slim_list_query(ontology: str):
    sparql.setQuery(get_slim_list_query(ontology))
    # TODO Add missing implementation
    pass


def run_slim_details_query():
    pass
