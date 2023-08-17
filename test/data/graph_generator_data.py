from rdflib import Literal, URIRef


def get_generate_enrichment_graph_data():
    return [
        {
            "s": "CL:0000809",
            "s_label": "double-positive, alpha-beta thymocyte",
            "p": "rdfs:subClassOf",
            "o": "CL:0000084",
            "o_label": "T cell",
        },
        {"s": "CL:0000813", "s_label": "memory T cell", "p": "rdfs:subClassOf", "o": "CL:0000084", "o_label": "T cell"},
        {
            "s": "CL:0000897",
            "s_label": "CD4-positive, alpha-beta memory T cell",
            "p": "rdfs:subClassOf",
            "o": "CL:0000084",
            "o_label": "T cell",
        },
        {
            "s": "CL:0000897",
            "s_label": "CD4-positive, alpha-beta memory T cell",
            "p": "rdfs:subClassOf",
            "o": "CL:0000813",
            "o_label": "memory T cell",
        },
        {
            "s": "CL:0000909",
            "s_label": "CD8-positive, alpha-beta memory T cell",
            "p": "rdfs:subClassOf",
            "o": "CL:0000084",
            "o_label": "T cell",
        },
        {
            "s": "CL:0000909",
            "s_label": "CD8-positive, alpha-beta memory T cell",
            "p": "rdfs:subClassOf",
            "o": "CL:0000813",
            "o_label": "memory T cell",
        },
    ]


def get_redundant_expected_triples():
    return [
        (
            URIRef("http://purl.obolibrary.org/obo/CL_0000909"),
            URIRef("http://www.w3.org/2000/01/rdf-schema#subClassOf"),
            URIRef("http://purl.obolibrary.org/obo/CL_0000813"),
        ),
        (
            URIRef("http://purl.obolibrary.org/obo/CL_0000813"),
            URIRef("http://www.w3.org/2000/01/rdf-schema#label"),
            Literal("memory T cell"),
        ),
        (
            URIRef("http://purl.obolibrary.org/obo/CL_0000813"),
            URIRef("http://www.w3.org/2000/01/rdf-schema#subClassOf"),
            URIRef("http://purl.obolibrary.org/obo/CL_0000084"),
        ),
        (
            URIRef("http://purl.obolibrary.org/obo/CL_0000897"),
            URIRef("http://www.w3.org/2000/01/rdf-schema#label"),
            Literal("CD4-positive, alpha-beta memory T cell"),
        ),
        (
            URIRef("http://purl.obolibrary.org/obo/CL_0000897"),
            URIRef("http://www.w3.org/2000/01/rdf-schema#subClassOf"),
            URIRef("http://purl.obolibrary.org/obo/CL_0000084"),
        ),
        (
            URIRef("http://purl.obolibrary.org/obo/CL_0000809"),
            URIRef("http://www.w3.org/2000/01/rdf-schema#subClassOf"),
            URIRef("http://purl.obolibrary.org/obo/CL_0000084"),
        ),
        (
            URIRef("http://purl.obolibrary.org/obo/CL_0000897"),
            URIRef("http://www.w3.org/2000/01/rdf-schema#subClassOf"),
            URIRef("http://purl.obolibrary.org/obo/CL_0000813"),
        ),
        (
            URIRef("http://purl.obolibrary.org/obo/CL_0000809"),
            URIRef("http://www.w3.org/2000/01/rdf-schema#label"),
            Literal("double-positive, alpha-beta thymocyte"),
        ),
        (
            URIRef("http://purl.obolibrary.org/obo/CL_0000909"),
            URIRef("http://www.w3.org/2000/01/rdf-schema#label"),
            Literal("CD8-positive, alpha-beta memory T cell"),
        ),
        (
            URIRef("http://purl.obolibrary.org/obo/CL_0000909"),
            URIRef("http://www.w3.org/2000/01/rdf-schema#subClassOf"),
            URIRef("http://purl.obolibrary.org/obo/CL_0000084"),
        ),
        (
            URIRef("http://purl.obolibrary.org/obo/CL_0000084"),
            URIRef("http://www.w3.org/2000/01/rdf-schema#label"),
            Literal("T cell"),
        ),
    ]


def get_nonredundant_expected_triples():
    return [
        (
            URIRef("http://purl.obolibrary.org/obo/CL_0000809"),
            URIRef("http://www.w3.org/2000/01/rdf-schema#label"),
            Literal("double-positive, alpha-beta thymocyte"),
        ),
        (
            URIRef("http://purl.obolibrary.org/obo/CL_0000809"),
            URIRef("http://www.w3.org/2000/01/rdf-schema#subClassOf"),
            URIRef("http://purl.obolibrary.org/obo/CL_0000084"),
        ),
        (
            URIRef("http://purl.obolibrary.org/obo/CL_0000813"),
            URIRef("http://www.w3.org/2000/01/rdf-schema#subClassOf"),
            URIRef("http://purl.obolibrary.org/obo/CL_0000084"),
        ),
        (
            URIRef("http://purl.obolibrary.org/obo/CL_0000909"),
            URIRef("http://www.w3.org/2000/01/rdf-schema#label"),
            Literal("CD8-positive, alpha-beta memory T cell"),
        ),
        (
            URIRef("http://purl.obolibrary.org/obo/CL_0000897"),
            URIRef("http://www.w3.org/2000/01/rdf-schema#subClassOf"),
            URIRef("http://purl.obolibrary.org/obo/CL_0000813"),
        ),
        (
            URIRef("http://purl.obolibrary.org/obo/CL_0000084"),
            URIRef("http://www.w3.org/2000/01/rdf-schema#label"),
            Literal("T cell"),
        ),
        (
            URIRef("http://purl.obolibrary.org/obo/CL_0000813"),
            URIRef("http://www.w3.org/2000/01/rdf-schema#label"),
            Literal("memory T cell"),
        ),
        (
            URIRef("http://purl.obolibrary.org/obo/CL_0000909"),
            URIRef("http://www.w3.org/2000/01/rdf-schema#subClassOf"),
            URIRef("http://purl.obolibrary.org/obo/CL_0000813"),
        ),
        (
            URIRef("http://purl.obolibrary.org/obo/CL_0000897"),
            URIRef("http://www.w3.org/2000/01/rdf-schema#label"),
            Literal("CD4-positive, alpha-beta memory T cell"),
        ),
    ]
