from typing import Optional


class Term:
    """Represents ontology terms."""

    def __init__(
        self,
        label: str,
        iri: str,
        is_valid: bool,
        new_label: Optional[str] = None,
        new_iri: Optional[str] = None,
    ):
        self.__label = label
        self.__iri = iri
        self.__is_valid = is_valid
        self.__new_label = new_label
        self.__new_iri = new_iri
        self.__is_obsolete: bool = True if new_label and new_iri else False

    def get_label(self) -> str:
        """Returns term label.

        Returns:
            Term label

        """
        return self.__label

    def get_iri(self) -> str:
        """Returns term IRI.

        Returns:
            Term IRI

        """
        return self.__iri

    def get_is_valid(self) -> bool:
        """Returns term validation status.

        Returns:
            True if term is valid False otherwise

        """
        return self.__is_valid

    def get_new_label(self) -> str:
        """Returns new term label of obsoleted term.

        Returns:
            New term label

        """
        return self.__new_label

    def get_new_iri(self) -> str:
        """Returns new term IRI of obsoleted term.

        Returns:
            New term IRI

        """
        return self.__new_iri

    def get_is_obsoleted(self) -> str:
        """Returns term obsoletion status.

        Returns:
            True if term is obsoleted False otherwise

        """
        return self.__is_obsolete

    def update_obsoleted_term(self):
        """Updates term label and IRI if the term is obsoleted, and changes its obsoletion status."""
        if self.__is_obsolete:
            self.__label = self.__new_label
            self.__iri = self.__new_iri
            self.__is_obsolete = False

    def __eq__(self, other):
        if isinstance(other, Term):
            return (
                self.__label == other.__label
                and self.__iri == other.__iri
                and self.__is_valid == other.__is_valid
                and self.__is_obsolete == other.__is_obsolete
                and (self.__new_label == other.__new_label if (self.__is_obsolete and other.__is_obsolete) else True)
                and (self.__new_iri == other.__new_iri if (self.__is_obsolete and other.__is_obsolete) else True)
            )
        return False

    def __str__(self):
        msg = f"IRI: {self.__iri}, Label: {self.__label}, Valid: {self.__is_valid}"
        if self.__is_valid:
            msg += f", Obsoleted: {self.__is_obsolete}"
        if self.__is_obsolete:
            msg += f", New term label: {self.__new_label}, New term IRI: {self.__new_iri}"
        return msg
