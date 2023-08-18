from pandasaurus.utils.sparql_queries import (
    get_contextual_enrichment_query,
    get_full_enrichment_query,
    get_label_query,
    get_replaced_by_query,
    get_simple_enrichment_query,
    get_slim_list_query,
    get_slim_members_query,
    get_synonym_query,
)


def test_get_simple_enrichment_query():
    s_iri_list = ["CL:0000084", "CL:0000787"]
    o_iri_list = ["CL:0000788", "CL:0000798"]
    property_list = ["rdfs:subClassOf"]

    query = get_simple_enrichment_query(s_iri_list, o_iri_list, property_list)

    expected_query = (
        "SELECT ?s ?s_label ?p ?o ?o_label WHERE { GRAPH <http://reasoner.renci.org/redundant> {"
        "VALUES ?s { CL:0000084 CL:0000787 } VALUES ?o { CL:0000788 CL:0000798 } VALUES ?p { rdfs:subClassOf }"
        "?s ?p ?o. } ?s rdfs:label ?s_label. ?o rdfs:label ?o_label. FILTER(?s != ?o)}# LIMIT"
    )

    assert query == expected_query


def test_get_minimal_enrichment_query():
    pass


def test_get_full_enrichment_query():
    s_iri_list = ["CL:0000084", "CL:0000787"]
    o_iri_list = ["CL:0000788", "CL:0000798"]

    query = get_full_enrichment_query(s_iri_list, o_iri_list)

    expected_query = (
        "SELECT DISTINCT ?s ?s_label ?p ?x ?x_label ?o ?o_label WHERE { GRAPH "
        "<http://reasoner.renci.org/nonredundant> { VALUES ?s { CL:0000084 CL:0000787 } VALUES ?o {  "
        "CL:0000788 CL:0000798 }  ?s rdfs:subClassOf* ?x. ?x rdfs:subClassOf* ?o. FILTER(?s != ?x)} ?s  "
        "rdfs:label ?s_label. ?x rdfs:label  ?x_label. ?o rdfs:label ?o_label }# LIMIT"
    )
    assert query == expected_query


def test_get_contextual_enrichment_query():
    context_list = ["UBERON:0000362", "UBERON:0002113"]

    query = get_contextual_enrichment_query(context_list)

    expected_query = (
        "SELECT * WHERE { VALUES ?context {UBERON:0000362 UBERON:0002113 } ?term BFO:0000050 ?context. ?term "
        "rdfs:subClassOf CL:0000000. ?term rdfs:label ?label }# LIMIT"
    )

    assert query == expected_query


def test_get_curie_prefix_validation_query():
    pass


def test_get_label_query():
    term_iri_list = ["CL:0000084", "CL:0000787"]

    query = get_label_query(term_iri_list)

    expected_query = (
        "SELECT ?term ?label where { ?term rdf:type owl:Class. OPTIONAL {?term rdfs:label ?label.} "
        "VALUES ?term { CL:0000084 CL:0000787} }# LIMIT"
    )

    assert query == expected_query


def test_get_synonym_query():
    term_iri_list = ["term1", "term2", "term3"]
    expected_query = (
        "SELECT * WHERE {VALUES ?s { term1 term2 term3 }{ OPTIONAL { ?s oio:hasNarrowSynonym ?narrow_synonym } } "
        "UNION { OPTIONAL { ?s oio:hasExactSynonym ?exact_synonym } } "
        "UNION { OPTIONAL {?s oio:hasRelatedSynonym ?related_synonym} } "
        "UNION { OPTIONAL {?s oio:hasBroadSynonym ?broad_synonym} } } # LIMIT"
    )
    assert get_synonym_query(term_iri_list) == expected_query


def test_get_obsolete_term_query():
    pass


def test_get_replaced_by_query():
    term_iri_list = ["CL:0000084", "CL:0000787"]

    query = get_replaced_by_query(term_iri_list)

    expected_query = (
        "SELECT * WHERE { ?term rdfs:label ?label. ?term owl:deprecated ?depr_status. ?term IAO:0100001 "
        "?new_term. ?new_term rdfs:label ?new_term_label VALUES ?term {CL:0000084 CL:0000787} }# LIMIT"
    )

    assert query == expected_query


def test_get_slim_list_query():
    ontology_name = "ontology_name"

    query = get_slim_list_query(ontology_name)

    expected_query = (
        "SELECT DISTINCT ?slim ?label ?comment WHERE { GRAPH ?ontology { ?ontology a owl:Ontology. "
        "?ontology <http://purl.org/dc/elements/1.1/title> ?title. ?term oio:inSubset ?slim. "
        "?slim rdfs:label ?label. ?slim rdfs:comment ?comment. FILTER(str(?title) = 'ontology_name') } }# LIMIT"
    )

    assert query == expected_query


def test_get_slim_members_query():
    slim_name = "slim_name"

    query = get_slim_members_query(slim_name)

    expected_query = (
        "SELECT ?term WHERE { ?term oio:inSubset ?slim. ?slim rdfs:label "
        "?slim_name. FILTER(str(?slim_name) = 'slim_name') }# LIMIT"
    )

    assert query == expected_query
