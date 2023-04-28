from typing import List

from .term import Term


class Slim:
    """Represents upper level slims"""

    def __init__(self, name: str, description: str, term_list: List[Term]):
        self.name = name
        self.description = description
        self.term_list = term_list

    def get_name(self) -> str:
        """

        Returns:
            str: Slim name

        """
        return self.name

    def get_description(self) -> str:
        """

        Returns:
            str: Slim description

        """
        return self.description

    def get_term_list(self) -> List[Term]:
        """

        Returns:
            List[Term]: Term list

        """
        return self.term_list

    def __str__(self):
        return f"Name:{self.name}, Description: {self.description}"
