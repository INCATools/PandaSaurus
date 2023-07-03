from typing import Dict, List

from pandasaurus.resources.slim import Slim
from pandasaurus.utils.pandasaurus_exceptions import InvalidOntology
from pandasaurus.utils.query_utils import run_sparql_query
from pandasaurus.utils.sparql_queries import (
    get_ontology_list_query,
    get_slim_list_query,
    get_slim_members_query,
)


class SlimManager:
    """SlimManager responsible for slim operations such as finding available slim in given ontologies and showing slim
    content.
    """

    # Might not be needed
    @staticmethod
    def get_slim_list(ontology: str) -> List[Dict[str, str]]:
        """Returns name and definition of available slims in given ontology.

        Args:
            ontology: Ontology name

        Returns:
            Slim names and definitions list

        """
        ontology_list = SlimManager._get_ontology_list()
        if ontology in ontology_list:
            slim_list: Dict[str, Slim] = dict()
            result = run_sparql_query(get_slim_list_query(ontology))
            for res in result:
                slim_list.update({res.get("label"): Slim(name=res.get("label"), description=res.get("comment"))})
            return [{"name": slim.get_name(), "description": slim.get_description()} for slim in slim_list.values()]
        raise InvalidOntology(ontology, ontology_list)

    @staticmethod
    def get_slim_members(slim_list: List[str]) -> List[str]:
        """Lists names and IDs of all terms in slim.

        Args:
            slim_list: A list of slim names

        Returns:
            Term IRIs of the slim members

        """
        return [
            term.get("term") for slim_name in slim_list for term in run_sparql_query(get_slim_members_query(slim_name))
        ]

    @staticmethod
    def _get_ontology_list():
        return [row.get("title") for row in run_sparql_query(get_ontology_list_query())]
