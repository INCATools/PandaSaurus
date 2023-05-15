from typing import Dict, List

from .resources.slim import Slim
from .resources.term import Term
from .utils.query_utils import run_sparql_query
from .utils.sparql_queries import get_slim_list_query, get_slim_members_query


class SlimManager:
    """SlimManager responsible for slim operations such as finding available slim in given ontologies and showing slim
    content.
    """

    @staticmethod
    def get_slim_list(ontology: str) -> List[Dict[str, str]]:
        """Returns name and definition of available slims in given ontology.

        Args:
            ontology: Ontology name

        Returns:
            Slim names and definitions list

        """
        slim_list: Dict[str, Slim] = dict()
        result = run_sparql_query(get_slim_list_query(ontology))
        for res in result:
            slim_list.update(
                {res.get("label"): Slim(name=res.get("label"), description=res.get("comment"))}
            )
        # slim_list = slim_list if not slim_list else slim_list.update(slim_list)
        # We probably need a good print method here instead of returning a list of list here.
        return [
            {"name": slim.get_name(), "description": slim.get_description()}
            for slim in slim_list.values()
        ]

    @staticmethod
    def get_slim_members(slim_list: List[str]) -> List[str]:
        """Lists names and IDs of all terms in slim.

        Args:
            slim_list: A list of slim names

        Returns:
            Term IRIs of the slim members

        """
        # We probably need a good print method here instead of returning a list of list here.

        return [
            term.get("term")
            for slim_name in slim_list
            for term in run_sparql_query(get_slim_members_query(slim_name))
        ]
        # return [term.get("term") for term in run_sparql_query(get_slim_members_query(slim_name))]
