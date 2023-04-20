from .resources.slim import Slim
from typing import Dict
from utils.query_utils import (
    run_slim_list_query,
    run_slim_details_query
)


class SlimManager:
    """

    """

    def __init__(self):
        self.slim_list: Dict[str, Slim] = dict()

    def find_slim_list(self, ontology: str):
        slim_list: Dict[str, Slim] = dict()
        # TODO Add missing implementation
        self.slim_list = slim_list

    def show_slim_content(self, slim_name: str):
        slim: Slim = self.slim_list.get(slim_name)
        # TODO Add missing implementation
        pass
