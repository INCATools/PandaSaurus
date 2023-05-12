from typing import Dict, List

from .resources.slim import Slim
from .resources.term import Term
from .utils.query_utils import run_sparql_query
from .utils.sparql_queries import get_slim_list_query, get_slim_members_query


class SlimManager:
    """SlimManager responsible for slim operations such as finding available slim in given ontologies and showing slim
    content.
    """

    def __init__(self):
        self.slim_list: Dict[str, Slim] = dict()

    def get_slim_list(self, ontology: str) -> List[Dict[str, str]]:
        """Returns name and definition of available slims in given ontology.

        Args:
            ontology: Ontology name

        Returns:
            Slim names and definitions list

        """
        # TODO Need review
        slim_list: Dict[str, Slim] = dict()
        result = run_sparql_query(get_slim_list_query(ontology))
        for res in result:
            slim_list.update(
                {res.get("label"): Slim(name=res.get("label"), description=res.get("comment"))}
            )
        self.slim_list = slim_list if not self.slim_list else self.slim_list.update(slim_list)
        # We probably need a good print method here instead of returning a list of list here.
        return [
            {"name": slim.get_name(), "description": slim.get_description()}
            for slim in self.slim_list.values()
        ]

    def get_slim_members(self, slim_name: str) -> List[List[str]]:
        """Lists names and IDs of all terms in slim.

        Args:
            slim_name: Slim name

        Returns:
            Term names and IDs of the slim

        """
        slim: Slim = self.slim_list.get(slim_name)
        result = run_sparql_query(get_slim_members_query(slim_name))
        if slim:
            slim.set_term_list(
                [Term(res.get("term_label"), res.get("term"), True) for res in result]
            )
        else:
            row = next(result)
            slim = Slim(
                slim_name, row.get("comment"), [Term(row.get("term_label"), row.get("term"), True)]
            )
            slim.set_term_list(
                [Term(res.get("term_label"), res.get("term"), True) for res in result]
            )
        # We probably need a good print method here instead of returning a list of list here.
        return slim.get_term_list()
