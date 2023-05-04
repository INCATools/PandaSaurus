import logging
from typing import List

import pandas as pd
from utils.query_utils import (
    retrieve_contextual_slim_triples,
    retrieve_full_slim_triples,
    retrieve_minimal_slim_triples,
    retrieve_simple_slim_triples,
)


class Query:
    """Query class is responsible for generating a pandas DataFrame that enriches the seed list with synonyms and
    all inferred subClassOf relationships between terms in the seed. It also allows queries over the DataFrame.

    Attributes:
        enriched_df (str): DataFrame that is enriched with synonyms and inferred relationships between terms in
        the seed. It will be used in further filtered queries.

    """

    def __init__(self, seed_list: List[str], enrichment_property_list: List[str] = []):
        """A Query object is initialised by passing a list of seed terms (where each term is a CURIE string,
        e.g. CL:0000001; all OBO standard CURIESs are recognised). It generates a pandas DataFrame that enriches the
        seed list with synonyms and all inferred subClassOf relationships by default, and it supports other
        relationships between terms in the seed. Additional methods allow enrichment with terms outside the seed
        from slims or specified by a semantic context.

        Args:
            seed_list (str): A list of seed terms where each term is a CURIE string
            enrichment_property_list (List[str]): Property list to extend enrichment queries

        """
        self.seed_list = seed_list
        self.enrichment_property_list = enrichment_property_list
        self.enriched_df: pd.DataFrame = pd.DataFrame()

    def simple_enrichment(self) -> pd.DataFrame:
        """Returns a DataFrame that is enriched with synonyms and inferred relationships between terms in the seed.
        Subject and object terms are members of the seed terms.

        Returns:
             pd.Dataframe: Enriched DataFrame

        """
        logging.info(self.seed_list)
        df = pd.DataFrame()
        # TODO Add missing implementation
        self.enriched_df = df
        return self.enriched_df

    def minimal_slim_enrichment(self, slim_list: List[str]) -> pd.DataFrame:
        """Returns a DataFrame that is enriched with synonyms and inferred relationships between terms in the seed list
        and in an extended seed list. The extended seed list consists of terms from the seed list and terms from
        given slim lists, classes tagged with some specified ‘subset’ axiom.

        Args:
            slim_list (List[str]): Slim list that consists of classes tagged with some specified ‘subset’ axiom

        Returns:
            pd.Dataframe: Enriched DataFrame

        """
        logging.info(self.seed_list)
        df = pd.DataFrame()
        # TODO Add missing implementation
        self.enriched_df = df
        return self.enriched_df

    def full_slim_enrichment(self, slim_list: List[str]) -> pd.DataFrame:
        """Returns a DataFrame that is enriched with synonyms and inferred relationships between terms in the seed list
        and in an extended seed list. The extended seed list consists of terms from the seed list and terms from
        given slim lists, classes tagged with some specified ‘subset’ axiom, with inferred terms via transitive
        subClassOf queries.

        Args:
             slim_list (List[str]): Slim list that consists of classes tagged with some specified ‘subset’ axiom

         Returns:
             pd.Dataframe: Enriched DataFrame

        """
        logging.info(self.seed_list)
        df = pd.DataFrame()
        # TODO Add missing implementation
        self.enriched_df = df
        return self.enriched_df

    def contextual_slim_enrichment(self, context: List[str]) -> pd.DataFrame:
        """Returns a Dataframe that is enriched with synonyms and inferred relationships between terms in the seed list
        and in an extended seed list. The extended seed list consists of terms from the seed list and all terms
        satisfied by some set of existential restrictions in the ubergraph (e.g. part_of 'Kidney').

        Args:
            context: Organ/tissue/multicellular anatomical structure list to determine the redundant graph via
            existential restrictions

        Returns:
            pd.Dataframe: Enriched Dataframe

        """
        logging.info(self.seed_list)
        df = pd.DataFrame()
        # TODO Add missing implementation
        self.enriched_df = df
        return self.enriched_df

    def query(self, column_name: str, query_term: str) -> pd.DataFrame:
        """Returns filtered dataframe via join on column to subject of enriched_df, looking up of object name or
        synonym via query of name_lookup

        Args:
            column_name (str): Column name
            query_term (str): Object label or synonym

        Returns:
            pd.Dataframe: Filtered Dataframe

        """
        df = self.enriched_df
        # TODO Add missing implementation
        return df
