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
    get_ancestor_enrichment_query,
    get_contextual_enrichment_query,
    get_full_enrichment_query,
    get_most_specific_objects_query,
    get_most_specific_subjects_query,
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
        self._seed_list = seed_list
        self._enrichment_property_list = enrichment_property_list if enrichment_property_list else ["rdfs:subClassOf"]
        self._term_list: List[Term] = CurieValidator.construct_term_list(seed_list)
        self.enriched_df = pd.DataFrame()
        self.graph_df = pd.DataFrame()
        self.graph = Graph()
        # Validation and reporting
        try:
            CurieValidator.get_validation_report(self._term_list)
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
        source_list = [term.get_iri() for term in self._term_list]
        object_list = source_list
        query_string = get_simple_enrichment_query(source_list, object_list, self._enrichment_property_list)
        self.enriched_df = (
            pd.DataFrame(
                [res for res in run_sparql_query(query_string)],
                columns=["s", "s_label", "p", "o", "o_label"],
            )
            .sort_values("s")
            .reset_index(drop=True)
        )
        self._generate_enrichment_graph(object_list)

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
        source_list = [term.get_iri() for term in self._term_list]
        object_list = list(set(source_list + SlimManager.get_slim_members(slim_list)))
        s_result = []
        for chunk in chunks(object_list, 90):
            s_result.extend(
                [
                    res
                    for res in run_sparql_query(
                        get_simple_enrichment_query(source_list, chunk, self._enrichment_property_list)
                    )
                ]
            )
        self.enriched_df = (
            pd.DataFrame(s_result, columns=["s", "s_label", "p", "o", "o_label"])
            .sort_values("s")
            .reset_index(drop=True)
        )
        self._generate_enrichment_graph(object_list)

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
        source_list = [term.get_iri() for term in self._term_list]
        object_list = list(set(source_list + SlimManager.get_slim_members(slim_list)))
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
        self._generate_enrichment_graph(object_list)

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
        source_list = [term.get_iri() for term in self._term_list]
        object_list = list(set(source_list + [res.get("term") for res in run_sparql_query(query_string)]))
        s_result = []
        for chunk in chunks(object_list, 90):
            s_result.extend(
                [
                    res
                    for res in run_sparql_query(
                        get_simple_enrichment_query(source_list, chunk, self._enrichment_property_list)
                    )
                ]
            )

        self.enriched_df = (
            pd.DataFrame(s_result, columns=["s", "s_label", "p", "o", "o_label"])
            .sort_values("s")
            .reset_index(drop=True)
        )
        self._generate_enrichment_graph(object_list)

        return self.enriched_df

    def ancestor_enrichment(self, step_count: str) -> pd.DataFrame:
        """
        Perform ancestor enrichment analysis with a specified number of hops.

        Args:
            step_count (str): The number of hops to consider when enriching terms.

        Returns:
            pd.DataFrame: A DataFrame containing enriched terms and associated information.

        This method conducts an ancestor enrichment analysis on a set of seed terms,
        considering the specified number of hops in the ontology graph. The analysis
        retrieves terms that are ancestors of the seed terms within the specified
        number of hops and compiles the results into a DataFrame.

        The `step_count` parameter controls the depth of the analysis. A smaller
        `step_count` limits the analysis to immediate ancestors, while a larger value
        includes more distant ancestors.

        """
        source_list = [term.get_iri() for term in self._term_list]
        query_string = get_ancestor_enrichment_query(source_list, step_count)
        object_list = list(set(uri for res in run_sparql_query(query_string) for uri in res.values()))
        s_result = []
        for chunk in chunks(object_list, 90):
            s_result.extend(
                [
                    res
                    for res in run_sparql_query(
                        get_simple_enrichment_query(source_list, chunk, self._enrichment_property_list)
                    )
                ]
            )

        self.enriched_df = (
            pd.DataFrame(s_result, columns=["s", "s_label", "p", "o", "o_label"])
            .sort_values("s")
            .reset_index(drop=True)
        )
        self._generate_enrichment_graph(object_list)

        return self.enriched_df

    def parent_enrichment(self):
        """
        Perform parent enrichment analysis.

        This method is a convenience wrapper around the `ancestor_enrichment` method,
        specifically designed to perform parent enrichment analysis. Parent enrichment
        analysis considers only immediate parent terms of the seed terms in the ontology
        graph (i.e., one-hop ancestors).

        Returns:
            pd.DataFrame: A DataFrame containing enriched parent terms and associated
            information.

        This method simplifies the process of conducting parent enrichment analysis by
        calling the `ancestor_enrichment` method with a `step_count` of 1, which limits
        the analysis to immediate parent terms of the seed terms.

        """
        self.ancestor_enrichment(1)

    def synonym_lookup(self) -> pd.DataFrame:
        """

        Returns:
            A DataFrame containing labels and synonyms of the terms from the seed list.

        """
        label_df = pd.DataFrame(
            {term.get_iri(): term.get_label() for term in self._term_list}.items(), columns=["ID", "label"]
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

    def get_most_specific_objects(self, predicate: str, ontology: str):
        """

        Args:
            predicate: Relationship that wanted to be explored
            ontology: PURL of obo ontologies in Ubergraph.

        Examples:
            Example Ontology PURLs:
                - http://purl.obolibrary.org/obo/cl.owl \n
                - http://purl.obolibrary.org/obo/uberon.owl

        Returns:

        """
        subject_list = [term.get_iri() for term in self._term_list]
        query_string = get_most_specific_objects_query(subject_list, predicate, ontology)
        return (
            pd.DataFrame(
                [res for res in run_sparql_query(query_string)],
                columns=["s", "s_label", "p", "o", "o_label"],
            )
            .sort_values("s")
            .reset_index(drop=True)
        )

    def get_most_specific_subjects(self, predicate: str, ontology: str):
        """

        Args:
            predicate: Relationship that wanted to be explored
            ontology: PURL of obo ontologies in Ubergraph.

        Examples:
            Example Ontology PURLs:
                - http://purl.obolibrary.org/obo/cl.owl \n
                - http://purl.obolibrary.org/obo/uberon.owl

        Returns:

        """
        object_list = [term.get_iri() for term in self._term_list]
        query_string = get_most_specific_subjects_query(object_list, predicate, ontology)
        return (
            pd.DataFrame(
                [res for res in run_sparql_query(query_string)],
                columns=["s", "s_label", "p", "o", "o_label"],
            )
            .sort_values("s")
            .reset_index(drop=True)
        )

    def query(self, column_name: str, query_term: str) -> pd.DataFrame:
        """Returns filtered dataframe via join on column to subject of enriched_df, looking up of object name or
        synonym via query of name_lookup.

        Args:
            column_name: Column name
            query_term: Object label or synonym

        Returns:
            Filtered DataFrame

        """
        # TODO Add missing implementation
        raise NotImplementedError

    def update_obsoleted_terms(self):
        """Replaces all obsoleted terms in the term list with the new term that obsoletes them."""
        [getattr(term, "update_obsoleted_term")() for term in self._term_list]

    def mirror_enrichment_for_graph_generation(self, term_list: List[str]):
        # TODO definitely need a refactoring later on
        s_result = []
        for s_chunk in chunks(term_list, 45):
            for o_chunk in chunks(term_list, 45):
                s_result.extend(
                    [
                        res
                        for res in run_sparql_query(
                            get_simple_enrichment_query(s_chunk, o_chunk, self._enrichment_property_list)
                        )
                    ]
                )
        self.graph_df = (
            pd.DataFrame(s_result, columns=["s", "s_label", "p", "o", "o_label"])
            .sort_values("s")
            .reset_index(drop=True)
        )

    def _generate_enrichment_graph(self, object_list):
        self.mirror_enrichment_for_graph_generation(object_list)
        self.graph = GraphGenerator.generate_enrichment_graph(self.graph_df)
        self.graph = GraphGenerator.apply_transitive_reduction(self.graph, self.enriched_df["p"].unique().tolist())
