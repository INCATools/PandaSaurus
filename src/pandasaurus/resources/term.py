class Term:
    """Represents ontology terms
    """

    def __init__(self, label: str, iri: str):
        self.label = label
        self.iri = iri

    def get_name(self) -> str:
        """

        Returns:
            str: Term label

        """
        return self.label

    def get_iri(self) -> str:
        """

        Returns:
            str: Term IRI

        """
        return self.iri

    def __str__(self):
        return f"{self.iri} {self.label}"
