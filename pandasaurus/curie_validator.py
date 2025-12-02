from abc import abstractmethod
from typing import Any, Dict, List, Optional, Union

from pandasaurus.resources.term import Term
from pandasaurus.utils.pandasaurus_exceptions import InvalidTerm, ObsoletedTerm
from pandasaurus.utils.query_utils import chunks, run_sparql_query
from pandasaurus.utils.sparql_queries import get_label_query, get_replaced_by_query


class CurieValidator:
    """CurieValidator is responsible for validating CURIE prefixes and CURIEs of slim terms. It also suggests
    replacements for obsoleted slim terms.
    """

    _CURIE_CHUNK_SIZE = 90

    @staticmethod
    @abstractmethod
    def validate_curie_prefixes(curie_list: List[str]) -> Dict[str, bool]:
        """Reports whether the CURIE prefixes are valid or not.

        Args:
            curie_list: List of CURIEs

        Returns:
            True or False status of the prefix validation for each term

        """
        # Is there anyway to validate prefixes via Ubergraph or are we going to validate them via a config file? OAK?
        # Do we still need this? https://github.com/INCATools/PandaSaurus/issues/1#issuecomment-1527753655
        # TODO Add missing implementation
        raise NotImplementedError

    @staticmethod
    def validate_curie_list(curie_list: List[str]) -> dict[str, dict[str, Union[Optional[bool], Any]]]:
        """Reports whether the CURIEs are valid or not.

        Args:
            curie_list: List of CURIEs

        Examples:
            | An example output that shows 2 valid and 1 invalid CURIEs:
            | {'CL:0002681': {'label': 'kidney cortical cell', 'valid': True},
            |  'CL:0002518': {'label': 'kidney epithelial cell', 'valid': True},
            |  'CL:1234567': {'label': None, 'valid': False}}

        Returns:
            True or False status of the CURIE validation for each term

        """
        result_dict: Dict[str, Optional[str]] = {}
        for chunk in chunks(curie_list, CurieValidator._CURIE_CHUNK_SIZE):
            # Large lists are split up to avoid massive VALUES blocks in SPARQL queries.
            query_string = get_label_query(chunk)
            for res in run_sparql_query(query_string):
                term = res.get("term")
                if term:
                    result_dict[term] = res.get("label")
        return {
            curie: {
                "label": result_dict.get(curie) if curie in result_dict else None,
                "valid": True if curie in result_dict else False,
            }
            for curie in curie_list
        }

    @staticmethod
    def find_obsolete_terms(curie_list: List[str]) -> Dict:
        """Returns obsoleted terms in the curie_list and label and IRI for of the term that is replaced the obsoleted
        terms.

        Args:
            curie_list: List of CURIEs

        Examples:
            | An example output that shows 1 obsoleted CURIE:
            | {'CL:0011107': {'term': 'CL:0011107', 'label': 'obsolete Muller cell', depr_status': 'true',
            | 'new_term': 'CL:0000636', new_term_label': 'Mueller cell'}

        Returns:
            True or False status of the term for each term

        """
        result_dict: Dict[str, Dict[str, Any]] = {}
        for chunk in chunks(curie_list, CurieValidator._CURIE_CHUNK_SIZE):
            query_string = get_replaced_by_query(chunk)
            for res in run_sparql_query(query_string):
                term = res.get("term")
                if term:
                    result_dict[term] = res
        return result_dict

    @staticmethod
    @abstractmethod
    def find_obsolete_term_replacement(curie_list: Dict[str, str]) -> Dict[str, str]:
        """Suggests terms for each obsoleted terms in the curie_list.

        Args:
            curie_list: List of CURIEs

        Returns:
            List of suggested term

        """
        # TODO Add missing implementation
        # We probably don't need this method
        raise NotImplementedError

    @staticmethod
    def get_validation_report(term_list: List[Term]):
        """Returns validation report which includes invalid and obsoleted terms.

        Args:
            term_list: A list of seed terms where each term is a Term object

        """
        invalid_terms: List[Term] = []
        obsoleted_terms: List[Term] = []
        for term in term_list:
            if not term.get_is_valid():
                invalid_terms.append(term)
            if term.get_is_obsoleted():
                obsoleted_terms.append(term)

        if invalid_terms:
            raise InvalidTerm(invalid_terms)
        if obsoleted_terms:
            raise ObsoletedTerm(obsoleted_terms)

    @staticmethod
    def construct_term_list(seed_list) -> List[Term]:
        """Returns list of Term objects after running validate_curie_list and find_obsolete_terms methods.

        Args:
            seed_list: A list of seed terms where each term is a CURIE string

        Returns:
            List of Term objects

        """
        term_validation = CurieValidator.validate_curie_list(seed_list)
        term_obsoletion = CurieValidator.find_obsolete_terms(seed_list)
        term_list: List[Term] = list()
        for seed in seed_list:
            validation_entry = term_validation.get(seed, {"label": None, "valid": False})
            obsoletion_entry = term_obsoletion.get(seed, {})
            term = Term(
                validation_entry.get("label"),
                seed,
                bool(validation_entry.get("valid")),
                obsoletion_entry.get("new_term_label"),
                obsoletion_entry.get("new_term"),
            )
            term_list.append(term)
        return term_list
