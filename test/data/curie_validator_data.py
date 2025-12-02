from pandasaurus.resources.term import Term


def get_validate_curie_list_data():
    return ["CL:0002681", "CL:0002518", "CL:1234567", "CL:1000500"]


def get_validate_curie_list_result():
    return [
        {"label": "kidney epithelial cell", "term": "CL:0002518"},
        {"label": "kidney cortical cell", "term": "CL:0002681"},
        {"label": "kidney interstitial cell", "term": "CL:1000500"},
    ]


def get_expected_validate_curie_list():
    return {
        "CL:0002681": {"label": "kidney cortical cell", "valid": True},
        "CL:0002518": {"label": "kidney epithelial cell", "valid": True},
        "CL:1234567": {"label": None, "valid": False},
        "CL:1000500": {"label": "kidney interstitial cell", "valid": True},
    }


def get_find_obsolete_terms_data():
    return ["CL:0000337", "CL:0011107", "CL:0002371", "CL:0002150"]


def get_find_obsolete_terms_result():
    return [
        {
            "depr_status": "true",
            "label": "obsolete Muller cell",
            "new_term": "CL:0000636",
            "new_term_label": "Mueller cell",
            "term": "CL:0011107",
        }
    ]


def get_expected_find_obsolete_terms():
    return {
        "CL:0011107": {
            "term": "CL:0011107",
            "depr_status": "true",
            "new_term": "CL:0000636",
            "label": "obsolete Muller cell",
            "new_term_label": "Mueller cell",
        }
    }


def get_construct_term_list_data():
    return ["CL:0000084", "CL:0000787", "CL:0000788", "CL:0000798"]


def get_construct_term_list_result():
    return [
        {"label": "T cell", "term": "CL:0000084"},
        {"label": "memory B cell", "term": "CL:0000787"},
        {"label": "naive B cell", "term": "CL:0000788"},
        {"label": "gamma-delta T cell", "term": "CL:0000798"},
    ]


def get_expected_construct_term_list():
    return [
        Term("T cell", "CL:0000084", True),
        Term("memory B cell", "CL:0000787", True),
        Term("naive B cell", "CL:0000788", True),
        Term("gamma-delta T cell", "CL:0000798", True),
    ]


def get_construct_term_list_missing_validation_data():
    return ["CL:0000084", "CL:9999999"]


def get_construct_term_list_missing_validation_result():
    return [
        {"label": "T cell", "term": "CL:0000084"},
    ]


def get_expected_construct_term_list_missing_validation():
    return [
        Term("T cell", "CL:0000084", True),
        Term(None, "CL:9999999", False),
    ]
