from typing import List


# TODO might need to update the enrichment query method names
def get_simple_enrichment_query(s_iri_list: List[str], o_iri_list: List[str], property_list: List[str]) -> str:
    return (
        f"SELECT ?s ?s_label ?p ?o ?o_label WHERE {{ GRAPH <http://reasoner.renci.org/redundant> {{"
        f"VALUES ?s {{ {' '.join(s_iri_list)} }} VALUES ?o {{ {' '.join(o_iri_list)} }} "
        f"VALUES ?p {{ {' '.join(property_list)} }}"
        f"?s ?p ?o. }} ?s rdfs:label ?s_label. ?o rdfs:label ?o_label. FILTER(?s != ?o)}}# LIMIT"
    )


def get_minimal_enrichment_query(seed_list: List[str]) -> str:
    # TODO Add missing implementation. Might not be needed
    pass


def get_full_enrichment_query(s_iri_list: List[str], o_iri_list: List[str]) -> str:
    return (
        f"SELECT DISTINCT ?s ?s_label ?p ?x ?x_label ?o ?o_label WHERE {{ GRAPH "
        f"<http://reasoner.renci.org/nonredundant> {{ VALUES ?s {{ {' '.join(s_iri_list)} }} VALUES ?o {{ "
        f" {' '.join(o_iri_list)} }}  ?s rdfs:subClassOf* ?x. ?x rdfs:subClassOf* ?o. FILTER(?s != ?x)}} ?s  "
        f"rdfs:label ?s_label. ?x rdfs:label  ?x_label. ?o rdfs:label ?o_label }}# LIMIT"
    )


def get_contextual_enrichment_query(context_list: List[str]) -> str:
    # BFO:0000050 , part of
    return (
        f"SELECT * WHERE {{ VALUES ?context {{{' '.join(context_list)} }} ?term BFO:0000050 ?context. "
        f"?term rdfs:subClassOf CL:0000000. ?term rdfs:label ?label }}# LIMIT"
    )


def get_curie_prefix_validation_query(seed_list: List[str]) -> str:
    # TODO Add missing implementation. Might not be needed
    pass


def get_label_query(term_iri_list: List[str]) -> str:
    """Used for CURIE validation"""
    return (
        f"SELECT ?term ?label where {{ ?term rdf:type owl:Class. OPTIONAL {{?term rdfs:label ?label.}} "
        f"VALUES ?term {{ {' '.join(term_iri_list)}}} }}# LIMIT"
    )


def get_synonym_query(term_iri_list: List[str]) -> str:
    return (
        f"SELECT * WHERE {{VALUES ?s {{ {' '.join(term_iri_list)} }}"
        f"{{ OPTIONAL {{ ?s oio:hasNarrowSynonym ?narrow_synonym }} }} "
        f"UNION {{ OPTIONAL {{ ?s oio:hasExactSynonym ?exact_synonym }} }} "
        f"UNION {{ OPTIONAL {{?s oio:hasRelatedSynonym ?related_synonym}} }} "
        f"UNION {{ OPTIONAL {{?s oio:hasBroadSynonym ?broad_synonym}} }} }} # LIMIT"
    )


def get_obsolete_term_query(seed_list: List[str]) -> str:
    # TODO Add missing implementation. Might not be needed
    pass


def get_replaced_by_query(term_iri_list: List[str]) -> str:
    # IAO:0100001, term replaced by .
    return (
        f"SELECT * WHERE {{ ?term rdfs:label ?label. ?term owl:deprecated ?depr_status. "
        f"?term IAO:0100001 ?new_term. ?new_term rdfs:label ?new_term_label "
        f"VALUES ?term {{{' '.join(term_iri_list)}}} }}# LIMIT"
    )


# Might not be needed
def get_slim_list_query(ontology: str) -> str:
    return (
        f"SELECT DISTINCT ?slim ?label ?comment WHERE {{ GRAPH ?ontology {{ ?ontology a owl:Ontology. ?ontology "
        f"<http://purl.org/dc/elements/1.1/title> ?title. ?term oio:inSubset ?slim. ?slim rdfs:label ?label. "
        f"?slim rdfs:comment ?comment. FILTER(str(?title) = '{ontology}') }} }}# LIMIT"
    )


def get_slim_members_query(slim_name: str) -> str:
    return (
        f"SELECT ?term WHERE {{ ?term oio:inSubset ?slim. "
        f"?slim rdfs:label ?slim_name. FILTER(str(?slim_name) = '{slim_name}') }}# LIMIT"
    )


def get_ontology_list_query() -> str:
    return (
        "SELECT ?title "
        "WHERE { ?ontology a owl:Ontology. ?ontology <http://purl.org/dc/elements/1.1/title> ?title }# LIMIT"
    )
