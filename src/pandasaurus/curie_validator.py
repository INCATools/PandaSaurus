from typing import List
from utils.query_utils import (
    run_curie_prefix_query,
    run_curie_list_query,
    run_obsolete_term_query,
    run_replaced_by_query
)


class CurieValidator:
    """CurieValidator is responsible for validating CURIE prefixes and CURIEs of slim terms. It also suggests
    replacements for obsoleted slim terms.
    """

    def __init__(self):
        # We might also use Slim object in here
        pass

    @staticmethod
    def validate_curie_prefixes(curie_list: List[str]) -> List[List[str, bool]]:
        """Reports whether the CURIE prefixes are valid or not

        Args:
            curie_list: List of CURIEs

        Returns:
            List[List[str, bool]]: True or False status of the prefix validation for each term

        """
        # Is there anyway to validate prefixes via Ubergraph or are we going to validate them via a config file? OAK?
        run_curie_prefix_query(curie_list)
        # TODO Add missing implementation
        pass

    @staticmethod
    def validate_curie_list(curie_list: List[str]) -> List[List[str, bool]]:
        """Reports whether the CURIEs are valid or not

        Args:
            curie_list: List of CURIEs

        Returns:
            List[List[str, bool]]: True or False status of the CURIE validation for each term

        """
        run_curie_list_query(curie_list)
        # TODO Add missing implementation
        pass

    @staticmethod
    def find_obsolete_terms(curie_list: List[str]) -> List[List[str, bool]]:
        """Reports whether the terms in the curie_list are obsoleted or not

        Args:
            curie_list: List of CURIEs

        Returns:
            List[List[str, bool]]: True or False status of the term for each term

        """
        run_obsolete_term_query(curie_list)
        # TODO Add missing implementation
        pass

    @staticmethod
    def find_obsolete_term_replacement(curie_list: List[str, str]):
        """Suggests terms for each obsoleted terms in the curie_list

        Args:
            curie_list: List of CURIEs

        Returns:
            List[str, str]: List of suggested term

        """
        run_replaced_by_query(curie_list)
        # TODO Add missing implementation
        pass
