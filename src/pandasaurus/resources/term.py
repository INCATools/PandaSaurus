class Term:
    """

    """

    def __init__(self, label: str, iri: str):
        self.label = label
        self.iri = iri

    def get_name(self):
        return self.label

    def get_iri(self):
        return self.iri

    def __str__(self):
        return f"{self.iri} {self.label}"
