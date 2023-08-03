from typing import List

from pandasaurus.resources.term import Term


class InvalidTerm(Exception):
    def __init__(self, term_list: List[Term]):
        self.message = f"The following terms are invalid: {', '.join([term.get_iri() for term in term_list])}"
        super().__init__(self.message)


class ObsoletedTerm(Exception):
    def __init__(self, term_list: List[Term]):
        self.message = (
            f"The following terms are obsoleted: {', '.join([term.get_iri() for term in term_list])}, "
            f"and replaced by following terms: {', '.join([term.get_new_iri() for term in term_list])}. "
            f"Please consider using the new terms"
        )
        super().__init__(self.message)


class InvalidOntology(Exception):
    def __init__(self, input_ontology: str, ontology_list: List[str]):
        self.message = (
            f"The '{input_ontology}' ontology is invalid. \n"
            f"Please use one of the following ontologies: \n{', '.join(ontology_list)}"
        )
        super().__init__(self.message)
