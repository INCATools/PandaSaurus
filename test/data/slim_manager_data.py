def get_valid_ontology_expected_message():
    return [
        {
            "name": "blood_and_immune_upper_slim",
            "description": "a subset of general classes related to blood and the immune system, primarily of "
            "hematopoietic origin",
        },
        {
            "name": "eye_upper_slim",
            "description": "a subset of general classes related to specific cell types in the eye.",
        },
    ]


def get_ontology_list_result():
    return [
        {"title": "Ontology for the Anatomy of the Insect SkeletoMuscular system"},
        {"title": "Biological Spatial Ontology"},
        {"title": "Cell Ontology"},
        {"title": "Core Ontology for Biology and Biomedicine"},
        {"title": "Coleoptera Anatomy Ontology"},
        {"title": "Drosophila Phenotype Ontology (DPO)"},
        {"title": "Evidence & Conclusion Ontology (ECO)"},
        {"title": "Information Artifact Ontology (IAO)"},
        {"title": "Environment Exposure Ontology"},
        {"title": "The Environment Ontology"},
        {"title": "Drosophila Anatomy Ontology (DAO)"},
        {"title": "FlyBase Controlled Vocabulary (FBcv)"},
        {"title": "Drosophila Developmental Ontology"},
        {"title": "Fission Yeast Phenotype Ontology (FYPO)"},
        {"title": "Gene Ontology"},
        {"title": "Human Phenotype Ontology"},
        {"title": "Lepidoptera Anatomy Ontology"},
        {"title": "Medical Action Ontology"},
        {"title": "Mondo Disease Ontology"},
        {"title": "The Mammalian Phenotype Ontology"},
        {"title": "Ontology of Biological Attributes (OBA)"},
        {"title": "PATO - the Phenotype And Trait Ontology"},
        {"title": "Provisional Cell Ontology"},
        {"title": "Population and Community Ontology"},
        {"title": "OBO Relations Ontology"},
        {"title": "CL bridge to fbbt"},
        {"title": "Uberon bridge to fbbt"},
        {"title": "Uber-anatomy ontology"},
        {"title": "C. elegans Gross Anatomy Ontology"},
        {"title": "C. elegans Development Ontology"},
        {"title": "C elegans Phenotype Ontology"},
        {"title": "Zebrafish Anatomy Ontology (ZFA)"},
        {"title": "Ascomycete Phenotype Ontology (APO)"},
        {"title": "MHC Restriction Ontology"},
        {"title": "Collembola Anatomy Ontology"},
    ]


def get_get_slim_list_result():
    return [
        {
            "slim": "cl#blood:and:immune:upper:slim",
            "label": "blood_and_immune_upper_slim",
            "comment": "a subset of general classes related to blood and the immune system, primarily of "
            "hematopoietic origin",
        },
        {
            "slim": "cl#eye:upper:slim",
            "label": "eye_upper_slim",
            "comment": "a subset of general classes related to specific cell types in the eye.",
        },
    ]


def get_invalid_ontology_expected_message():
    return (
        "The 'Call Ontology' ontology is invalid. \n"
        "Please use one of the following ontologies: \n"
        "Ontology for the Anatomy of the Insect SkeletoMuscular system, Biological Spatial Ontology, Cell Ontology, "
        "Core Ontology for Biology and Biomedicine, Coleoptera Anatomy Ontology, Drosophila Phenotype Ontology (DPO), "
        "Evidence & Conclusion Ontology (ECO), Information Artifact Ontology (IAO), Environment Exposure Ontology, "
        "The Environment Ontology, Drosophila Anatomy Ontology (DAO), FlyBase Controlled Vocabulary (FBcv), "
        "Drosophila Developmental Ontology, Fission Yeast Phenotype Ontology (FYPO), Gene Ontology, "
        "Human Phenotype Ontology, Lepidoptera Anatomy Ontology, Medical Action Ontology, Mondo Disease Ontology, "
        "The Mammalian Phenotype Ontology, Ontology of Biological Attributes (OBA), PATO - the Phenotype And Trait "
        "Ontology, Provisional Cell Ontology, Population and Community Ontology, OBO Relations Ontology, CL bridge to "
        "fbbt, Uberon bridge to fbbt, Uber-anatomy ontology, C. elegans Gross Anatomy Ontology, C. elegans Development "
        "Ontology, C elegans Phenotype Ontology, Zebrafish Anatomy Ontology (ZFA), Ascomycete Phenotype Ontology "
        "(APO), MHC Restriction Ontology, Collembola Anatomy Ontology"
    )


def get_slim_list():
    return ["blood_and_immune_upper_slim"]


def get_slim_members_result():
    return [
        {"term": "CL:0000037"},
        {"term": "CL:0000038"},
        {"term": "CL:0000097"},
        {"term": "CL:0000145"},
        {"term": "CL:0000232"},
        {"term": "CL:0000233"},
        {"term": "CL:0000235"},
        {"term": "CL:0000236"},
        {"term": "CL:0000547"},
        {"term": "CL:0000556"},
        {"term": "CL:0000558"},
        {"term": "CL:0000576"},
        {"term": "CL:0000647"},
        {"term": "CL:0000762"},
        {"term": "CL:0000765"},
        {"term": "CL:0000767"},
        {"term": "CL:0000771"},
        {"term": "CL:0000775"},
        {"term": "CL:0000784"},
        {"term": "CL:0000786"},
        {"term": "CL:0000789"},
        {"term": "CL:0000798"},
        {"term": "CL:0000816"},
        {"term": "CL:0000837"},
        {"term": "CL:0000842"},
        {"term": "CL:0000889"},
        {"term": "CL:0000990"},
        {"term": "CL:0001065"},
        {"term": "CL:0002031"},
        {"term": "CL:0002032"},
        {"term": "CL:0002087"},
        {"term": "CL:0002420"},
        {"term": "CL:0002679"},
        {"term": "CL:0017005"},
        {"term": "CL:0017006"},
        {"term": "CL:4030029"},
    ]


def get_expected_slim_members():
    return [
        "CL:0000037",
        "CL:0000038",
        "CL:0000097",
        "CL:0000145",
        "CL:0000232",
        "CL:0000233",
        "CL:0000235",
        "CL:0000236",
        "CL:0000547",
        "CL:0000556",
        "CL:0000558",
        "CL:0000576",
        "CL:0000647",
        "CL:0000762",
        "CL:0000765",
        "CL:0000767",
        "CL:0000771",
        "CL:0000775",
        "CL:0000784",
        "CL:0000786",
        "CL:0000789",
        "CL:0000798",
        "CL:0000816",
        "CL:0000837",
        "CL:0000842",
        "CL:0000889",
        "CL:0000990",
        "CL:0001065",
        "CL:0002031",
        "CL:0002032",
        "CL:0002087",
        "CL:0002420",
        "CL:0002679",
        "CL:0017005",
        "CL:0017006",
        "CL:4030029",
    ]
