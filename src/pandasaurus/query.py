import logging
import pandas as pd
from typing import List
from utils.query_utils import (
    retrieve_simple_slim_triples,
    retrieve_minimal_slim_triples,
    retrieve_full_slim_triples,
    retrieve_contextual_slim_triples
)


class Query:
    """Query class is responsible for returning the non-redundant graph for s subClassOf o as a simple Pandas dataframe
    with given 2 seeds of classes, S(s) and S(o) from an initial seed, S(i)
    """

    def __init__(self, seed_list: List[str]):
        self.seed_list = seed_list
        self.enriched_df: pd.DataFrame = pd.DataFrame()

    def simple_enrichment(self) -> pd.DataFrame:
        """Returns simple enrichment; S(s) = S(i); S(o) = S(i)

        Returns:
             pd.Dataframe: Enriched df

        """
        logging.info(self.seed_list)
        df = pd.DataFrame()
        # TODO Add missing implementation
        self.enriched_df = df
        return self.enriched_df

    def minimal_slim_enrichment(self, slim_list: List[str]) -> pd.DataFrame:
        """Returns minimal enrichment; S(s) = S(i); S(o) = S(i) + all classes in some specified slims, where class
        in slim = class tagged with some specified ‘subset’ axiom


        Args:
            slim_list (List[str]): Slim list

        Returns:
            pd.Dataframe: Enriched df

        """
        logging.info(self.seed_list)
        df = pd.DataFrame()
        # TODO Add missing implementation
        self.enriched_df = df
        return self.enriched_df

    def full_slim_enrichment(self, slim_list: List[str]) -> pd.DataFrame:
        """Returns full slim enrichment; S(s) = S(i); S(o) = S(i) + all classes in some specified slims, where class
        in slim = class tagged with some specified ‘subset’ axiom, with transitive query of redundant graph such as
        owl:subClassOf*

       Args:
            slim_list (List[str]): Slim list

        Returns:
            pd.Dataframe: Enriched df

        """
        logging.info(self.seed_list)
        df = pd.DataFrame()
        # TODO Add missing implementation
        self.enriched_df = df
        return self.enriched_df

    def contextual_slim_enrichment(self, context: List[str]) -> pd.DataFrame:
        """Returns contextual slim enrichment; S(s) = S(i); S(o) = S(i) + all classes satisfied by some set of
        existential restrictions in the ubergraph redundant graph (e.g. part_of 'Kidney')

        Args:
            context: Organ/tissue/multicellular anatomical structure list to determine the redundant graph via
            existential restrictions

        Returns:
            pd.Dataframe: Enriched df

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
            pd.Dataframe: Filtered dataframe

        """
        df = self.enriched_df
        # TODO Add missing implementation
        return df
