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
    """
    Query class
    """

    def __init__(self, seed_list: List[str]):
        self.seed_list = seed_list
        # Not sure about this
        self.enriched_df = pd.DataFrame()

    def simple_slim_enrichment(self):
        logging.info(self.seed_list)
        df = pd.DataFrame()
        # TODO Add missing implementation
        self.enriched_df = df

    def minimal_slim_enrichment(self):
        logging.info(self.seed_list)
        df = pd.DataFrame()
        # TODO Add missing implementation
        self.enriched_df = df

    def full_slim_enrichment(self):
        logging.info(self.seed_list)
        df = pd.DataFrame()
        # TODO Add missing implementation
        self.enriched_df = df

    def contextual_slim_enrichment(self):
        logging.info(self.seed_list)
        df = pd.DataFrame()
        # TODO Add missing implementation
        self.enriched_df = df

    def query(self, column_name: str, query_term: str) -> pd.DataFrame:
        df = self.enriched_df
        # TODO Add missing implementation
        return df
