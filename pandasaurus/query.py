from typing import List, Optional

import pandas as pd
from rdflib import Graph

from pandasaurus.curie_validator import CurieValidator
from pandasaurus.graph.graph_generator import GraphGenerator
from pandasaurus.resources.term import Term
from pandasaurus.slim_manager import SlimManager
from pandasaurus.utils.pandasaurus_exceptions import InvalidTerm, ObsoletedTerm
from pandasaurus.utils.query_utils import chunks, run_sparql_query
from pandasaurus.utils.sparql_queries import (
    get_contextual_enrichment_query,
    get_full_enrichment_query,
    get_simple_enrichment_query,
    get_synonym_query,
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
        self.__enrichment_property_list = enrichment_property_list if enrichment_property_list else ["rdfs:subClassOf"]
        self.__term_list: List[Term] = CurieValidator.construct_term_list(seed_list)
        self.enriched_df = pd.DataFrame()
        self.graph_df = pd.DataFrame()
        self.graph = Graph()
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
        source_list = [term.get_iri() for term in self.__term_list]
        object_list = [term.get_iri() for term in self.__term_list]
        query_string = get_simple_enrichment_query(source_list, object_list, self.__enrichment_property_list)
        self.enriched_df = (
            pd.DataFrame(
                [res for res in run_sparql_query(query_string)],
                columns=["s", "s_label", "p", "o", "o_label"],
            )
            .sort_values("s")
            .reset_index(drop=True)
        )
        self.mirror_enrichment_for_graph_generation(object_list)
        self.graph = GraphGenerator.generate_enrichment_graph(self.graph_df)
        self.graph = GraphGenerator.apply_transitive_reduction(self.graph, self.graph_df["p"].unique().tolist())

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
        source_list = [term.get_iri() for term in self.__term_list]
        object_list = source_list + SlimManager.get_slim_members(slim_list)
        s_result = []
        for chunk in chunks(object_list, 90):
            s_result.extend(
                [
                    res
                    for res in run_sparql_query(
                        get_simple_enrichment_query(source_list, chunk, self.__enrichment_property_list)
                    )
                ]
            )
        self.enriched_df = (
            pd.DataFrame(s_result, columns=["s", "s_label", "p", "o", "o_label"])
            .sort_values("s")
            .reset_index(drop=True)
        )
        self.mirror_enrichment_for_graph_generation(object_list)
        self.graph = GraphGenerator.generate_enrichment_graph(self.graph_df)
        self.graph = GraphGenerator.apply_transitive_reduction(self.graph, self.enriched_df["p"].unique().tolist())

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
        source_list = [term.get_iri() for term in self.__term_list]
        object_list = source_list + SlimManager.get_slim_members(slim_list)
        s_result = []
        for chunk in chunks(object_list, 90):
            s_result.extend([res for res in run_sparql_query(get_full_enrichment_query(source_list, chunk))])

        self.enriched_df = (
            pd.DataFrame(s_result, columns=["s", "s_label", "p", "x", "x_label"])
            .rename(columns={"x": "o", "x_label": "o_label"})
            .fillna({"p": "rdfs:subClassOf"})
            .sort_values("s")
            .reset_index(drop=True)
        )
        self.mirror_enrichment_for_graph_generation(object_list)
        self.graph = GraphGenerator.generate_enrichment_graph(self.graph_df)
        self.graph = GraphGenerator.apply_transitive_reduction(self.graph, self.enriched_df["p"].unique().tolist())

        return self.enriched_df

    def contextual_slim_enrichment(self, context: List[str]) -> pd.DataFrame:
        """Returns a DataFrame that is enriched with synonyms and inferred relationships between terms in the seed list
        and in an extended seed list. The extended seed list consists of terms from the seed list and all terms
        satisfied by some set of existential restrictions in the ubergraph (e.g. part_of some 'kidney').

        Args:
            context: Organ/tissue/multicellular anatomical structure list to determine the redundant graph via
            existential restrictions. It must be a valid CURIE.

        Returns:
            Enriched DataFrame

        """
        # TODO add a curie checking mechanism for context list
        query_string = get_contextual_enrichment_query(context)
        source_list = [term.get_iri() for term in self.__term_list]
        object_list = source_list + [res.get("term") for res in run_sparql_query(query_string)]
        s_result = []
        for chunk in chunks(object_list, 90):
            s_result.extend(
                [
                    res
                    for res in run_sparql_query(
                        get_simple_enrichment_query(source_list, chunk, self.__enrichment_property_list)
                    )
                ]
            )

        self.enriched_df = (
            pd.DataFrame(s_result, columns=["s", "s_label", "p", "o", "o_label"])
            .sort_values("s")
            .reset_index(drop=True)
        )
        self.mirror_enrichment_for_graph_generation(object_list)
        self.graph = GraphGenerator.generate_enrichment_graph(self.graph_df)
        self.graph = GraphGenerator.apply_transitive_reduction(self.graph, self.enriched_df["p"].unique().tolist())

        return self.enriched_df

    def synonym_lookup(self) -> pd.DataFrame:
        """

        Returns:
            A DataFrame containing labels and synonyms of the terms from the seed list.

        """
        label_df = pd.DataFrame(
            {term.get_iri(): term.get_label() for term in self.__term_list}.items(), columns=["ID", "label"]
        )

        synonym_query_results = run_sparql_query(get_synonym_query(label_df["ID"].tolist()))
        synonym_df = (
            pd.DataFrame([res for res in synonym_query_results if any("synonym" in key for key in res.keys())])
            .melt(id_vars="s", var_name="type", value_name="name")
            .rename(columns={"s": "ID"})
            .dropna(subset=["name"])[["ID", "name", "type"]]
        )

        # Merging two df
        result_df = (
            pd.merge(synonym_df, label_df, on="ID", how="left")
            .sort_values("ID")
            .reset_index(drop=True)[["ID", "label", "name", "type"]]
        )

        return result_df

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

    def mirror_enrichment_for_graph_generation(self, term_list: List[str]):
        # TODO definitely need a refactoring later on
        s_result = []
        for s_chunk in chunks(term_list, 45):
            for o_chunk in chunks(term_list, 45):
                s_result.extend(
                    [
                        res
                        for res in run_sparql_query(
                            get_simple_enrichment_query(s_chunk, o_chunk, self.__enrichment_property_list)
                        )
                    ]
                )
        self.graph_df = (
            pd.DataFrame(s_result, columns=["s", "s_label", "p", "o", "o_label"])
            .sort_values("s")
            .reset_index(drop=True)
        )
