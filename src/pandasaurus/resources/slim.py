from .term import Term
from typing import List


class Slim:
    """

    """

    def __init__(self, name: str, description: str, term_list: List[Term]):
        self.name = name
        self.description = description
        self.term_list = term_list

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def get_term_list(self):
        return self.term_list

    def __str__(self):
        return f"Name:{self.name}, Description: {self.description}"
