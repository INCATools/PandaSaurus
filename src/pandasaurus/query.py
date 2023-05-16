import logging
from typing import List, Optional

import pandas as pd

from .curie_validator import CurieValidator
from .resources.term import Term
from .slim_manager import SlimManager
from .utils.pandasaurus_exceptions import InvalidTerm, ObsoletedTerm
from .utils.query_utils import chunks, run_sparql_query
from .utils.sparql_queries import (
    get_contextual_enrichment_query,
    get_full_enrichment_query,
    get_simple_enrichment_query,
)


class Query:
    """Query class is responsible for generating a pandas DataFrame that enriches the seed list with synonyms and
    all inferred subClassOf relationships between terms in the seed. It also allows queries over the DataFrame.

    Attributes:
        enriched_df: DataFrame that is enriched with synonyms and inferred relationships between terms in
        the seed. It will be used in further filtered queries.

    """

    def __init__(
        self,
        seed_list: List[str],
        enrichment_property_list: Optional[List[str]] = None,
        force_fail: bool = False,
    ):
        """A Query object is initialised by passing a list of seed terms (where each term is a CURIE string,
        e.g. CL:0000001; all OBO standard CURIESs are recognised). It generates a pandas DataFrame that enriches the
        seed list with synonyms and all inferred subClassOf relationships by default, and it supports other
        relationships between terms in the seed. Additional methods allow enrichment with terms outside the seed
        from slims or specified by a semantic context.

        Args:
            seed_list: A list of seed terms where each term is a CURIE string
            enrichment_property_list: Optional list of property IRIs to extend enrichment queries.

        """
        # Might be unnecessary
        self.__seed_list = seed_list
        self.__enrichment_property_list = enrichment_property_list
        self.enriched_df: pd.DataFrame = pd.DataFrame()
        self.__term_list: List[Term] = CurieValidator().construct_term_list(seed_list)
        # Validation and reporting
        try:
            CurieValidator.get_validation_report(self.__term_list)
        except InvalidTerm as e:
            print(e.message)
            if force_fail:
                raise ValueError("Check your seed list! It contains invalid terms")
        except ObsoletedTerm as e:
            print(e.message)
            if force_fail:
                raise ValueError(
                    "Check your seed list! It contains obsoleted terms. Use update_obsoleted_terms "
                    "method to update all obsoleted term"
                )

    def simple_enrichment(self) -> pd.DataFrame:
        """Returns a DataFrame that is enriched with synonyms and inferred relationships between terms in the seed.
        Subject and object terms are members of the seed terms.

        Returns:
             Enriched DataFrame

        """
        logging.debug(self.__seed_list)
        # Enrichment process
        source_list = [term.get_iri() for term in self.__term_list]
        object_list = [term.get_iri() for term in self.__term_list]
        query_string = get_simple_enrichment_query(
            source_list, object_list, self.__enrichment_property_list
        )
        self.enriched_df = pd.DataFrame(
            [res for res in run_sparql_query(query_string)],
            columns=["s", "s_label", "p", "o", "o_label"],
        )
        return self.enriched_df

    def minimal_slim_enrichment(self, slim_list: List[str]) -> pd.DataFrame:
        """Returns a DataFrame that is enriched with synonyms and inferred relationships between terms in the seed list
        and in an extended seed list. The extended seed list consists of terms from the seed list and terms from
        given slim lists, classes tagged with some specified ‘subset’ axiom.

        Args:
            slim_list: List 'subset' tags that consists of classes tagged with some specified ‘subset’ axiom

        Returns:
            Enriched DataFrame

        """
        logging.info(self.__seed_list)
        # Enrichment process
        source_list = [term.get_iri() for term in self.__term_list]
        object_list = source_list + SlimManager.get_slim_members(slim_list)
        s_result = []
        if len(object_list) > 90:
            for chunk in chunks(object_list, 90):
                s_result.extend(
                    [
                        res
                        for res in run_sparql_query(
                            get_simple_enrichment_query(
                                source_list, chunk, self.__enrichment_property_list
                            )
                        )
                    ]
                )
        else:
            s_result = [
                res
                for res in run_sparql_query(
                    get_simple_enrichment_query(
                        source_list, object_list, self.__enrichment_property_list
                    )
                )
            ]

        self.enriched_df = pd.DataFrame(s_result, columns=["s", "s_label", "p", "o", "o_label"])
        return self.enriched_df

    def full_slim_enrichment(self, slim_list: List[str]) -> pd.DataFrame:
        """Returns a DataFrame that is enriched with synonyms and inferred relationships between terms in the seed list
        and in an extended seed list. The extended seed list consists of terms from the seed list and terms from
        given slim lists, classes tagged with some specified ‘subset’ axiom, with inferred terms via transitive
        subClassOf queries.

        Args:
             slim_list: List 'subset' tags that consists of classes tagged with some specified ‘subset’ axiom

         Returns:
             Enriched DataFrame

        """
        logging.info(self.__seed_list)
        # Enrichment process
        source_list = [term.get_iri() for term in self.__term_list]
        object_list = source_list + SlimManager.get_slim_members(slim_list)
        s_result = []
        if len(object_list) > 90:
            for chunk in chunks(object_list, 90):
                s_result.extend(
                    [res for res in run_sparql_query(get_full_enrichment_query(source_list, chunk))]
                )
        else:
            s_result = [
                res for res in run_sparql_query(get_full_enrichment_query(source_list, object_list))
            ]
        self.enriched_df = pd.DataFrame(s_result, columns=["s", "s_label", "p", "o", "o_label"])
        return self.enriched_df

    def contextual_slim_enrichment(self, context: List[str]) -> pd.DataFrame:
        """Returns a DataFrame that is enriched with synonyms and inferred relationships between terms in the seed list
        and in an extended seed list. The extended seed list consists of terms from the seed list and all terms
        satisfied by some set of existential restrictions in the ubergraph (e.g. part_of some 'kidney').

        Args:
            context: Organ/tissue/multicellular anatomical structure list to determine the redundant graph via
            existential restrictions

        Returns:
            Enriched DataFrame

        """
        logging.info(self.__seed_list)
        # Enrichment process
        query_string = get_contextual_enrichment_query(context)
        source_list = [term.get_iri() for term in self.__term_list]
        object_list = source_list + [res.get("term") for res in run_sparql_query(query_string)]
        s_result = []
        if len(object_list) > 90:
            for chunk in chunks(object_list, 90):
                s_result.extend(
                    [
                        res
                        for res in run_sparql_query(
                            get_simple_enrichment_query(
                                source_list, chunk, self.__enrichment_property_list
                            )
                        )
                    ]
                )
        else:
            s_result = [
                res
                for res in run_sparql_query(
                    get_simple_enrichment_query(
                        source_list, object_list, self.__enrichment_property_list
                    )
                )
            ]

        self.enriched_df = pd.DataFrame(s_result, columns=["s", "s_label", "p", "o", "o_label"])
        return self.enriched_df

    def query(self, column_name: str, query_term: str) -> pd.DataFrame:
        """Returns filtered dataframe via join on column to subject of enriched_df, looking up of object name or
        synonym via query of name_lookup.

        Args:
            column_name: Column name
            query_term: Object label or synonym

        Returns:
            Filtered DataFrame

        """
        df = self.enriched_df
        # TODO Add missing implementation
        return df

    def update_obsoleted_terms(self):
        """Replaces all obsoleted terms in the term list with the new term that obsoletes them."""
        [getattr(term, "update_obsoleted_term")() for term in self.__term_list]
