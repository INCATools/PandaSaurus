from test.data.slim_manager_data import get_slim_list, get_valid_ontology_expected_message, get_ontology_list_result, \
    get_invalid_ontology_expected_message, get_get_slim_list_result, get_slim_members_result, get_expected_slim_members

import pytest

from pandasaurus.slim_manager import SlimManager
from pandasaurus.utils.pandasaurus_exceptions import InvalidOntology


def test_get_slim_list_valid_ontology(mocker):
    mocker.patch(
        "pandasaurus.slim_manager.run_sparql_query",
        side_effect=[
            iter(
                get_ontology_list_result()
            ),
            iter(
                get_get_slim_list_result()
            ),
        ],
    )
    assert SlimManager.get_slim_list("Cell Ontology") == get_valid_ontology_expected_message()


def test_get_slim_list_invalid_ontology(mocker):
    mocker.patch(
        "pandasaurus.slim_manager.run_sparql_query",
        side_effect=[
            iter(
                get_ontology_list_result()
            ),
        ],
    )

    with pytest.raises(InvalidOntology) as exc_info:
        SlimManager.get_slim_list("Call Ontology")

    assert str(exc_info.value) == get_invalid_ontology_expected_message()


def test_get_slim_members(mocker):
    slim_list = get_slim_list()
    mocker.patch(
        "pandasaurus.slim_manager.run_sparql_query",
        side_effect=[
            iter(
                get_slim_members_result()
            )
        ],
    )
    get_slim_members = SlimManager.get_slim_members(slim_list)

    assert get_slim_members == get_expected_slim_members()
