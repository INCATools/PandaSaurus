from typing import List, Optional

from pandasaurus.resources.term import Term


class Slim:
    """Represents upper level slims"""

    def __init__(self, name: str, description: str, term_list: Optional[List[Term]] = None):
        self._name = name
        self._description = description
        self._term_list = term_list

    def get_name(self) -> str:
        """

        Returns:
            str: Slim name

        """
        return self._name

    def get_description(self) -> str:
        """Returns slim description

        Returns:
            Slim description

        """
        return self._description

    def get_term_list(self) -> List[Term]:
        """Returns term list

        Returns:
            Term list

        """
        return self._term_list

    def set_term_list(self, term_list: List[Term]):
        """Sets term list"""
        self._term_list = term_list

    def __str__(self):
        return f"Name:{self._name}, Description: {self._description}"
