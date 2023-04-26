from .resources.slim import Slim
from typing import Dict, List
from utils.query_utils import (
    run_slim_list_query,
    run_slim_details_query
)


class SlimManager:
    """SlimManager responsible for slim operations such as finding available slim in given ontologies and showing slim
    content
    """

    def __init__(self):
        self.slim_list: Dict[str, Slim] = dict()

    def find_slim_list(self, ontology: str) -> List[List[str]]:
        """Returns name and definition of available slims in given ontology

        Args:
            ontology (str): Ontology name

        Returns:
            List[List[str]]: Slim names and definitions list

        """
        slim_list: Dict[str, Slim] = dict()
        # TODO Add missing implementation
        self.slim_list = slim_list
        # We probably need a good print method here instead of returning a list of list here.
        return [[slim.name, slim.description] for slim in self.slim_list]

    def show_slim_content(self, slim_name: str) -> List[List[str]]:
        """Lists names and IDs of all terms in slim.

        Args:
            slim_name (str): Slim name

        Returns:
            List[List[str]]: Term names and IDs of the slim

        """
        slim: Slim = self.slim_list.get(slim_name)
        # TODO Add missing implementation
        # We probably need a good print method here instead of returning a list of list here.
        return [[term.label, term.iri] for term in slim]
