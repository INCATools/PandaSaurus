from typing import List
from utils.query_utils import (
    run_curie_prefix_query,
    run_curie_list_query,
    run_obsolete_term_query,
    run_replaced_by_query
)


class CurieValidator:
    """

    """
    def __init__(self):
        pass

    @staticmethod
    def validate_curie_prefixes(curie_list: List[str]) -> bool:
        # curie list or curie prefix list?
        # Is there anyway to validate prefixes via Ubergraph or are we going to validate them via a config file?
        run_curie_prefix_query(curie_list)
        # TODO Add missing implementation
        pass

    @staticmethod
    def validate_curie_list(curie_list: List[str]) -> bool:
        run_curie_list_query(curie_list)
        # TODO Add missing implementation
        pass

    @staticmethod
    def find_obsolete_terms(curie_list: List[str]) -> bool:
        run_obsolete_term_query(curie_list)
        # TODO Add missing implementation
        pass

    @staticmethod
    def find_obsolete_term_replacement(curie_list: List[str]):
        run_replaced_by_query(curie_list)
        # TODO Add missing implementation
        pass
