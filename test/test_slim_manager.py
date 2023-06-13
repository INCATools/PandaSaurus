from src.pandasaurus.slim_manager import SlimManager


def test_get_slim_list(mocker):
    expected_get_slim_list = [
        {
            "name": "blood_and_immune_upper_slim",
            "description": "a subset of general classes related to blood and the immune system, primarily of "
            "hematopoietic origin",
        },
        {
            "name": "eye_upper_slim",
            "description": "a subset of general classes related to specific cell types in the eye.",
        },
    ]

    # Mocking the run_sparql_query function
    mocker.patch(
        "src.pandasaurus.slim_manager.run_sparql_query",
        return_value=iter(
            [
                {
                    "slim": "cl#blood:and:immune:upper:slim",
                    "label": "blood_and_immune_upper_slim",
                    "comment": "a subset of general classes related to blood and the immune system, primarily of "
                    "hematopoietic origin",
                },
                {
                    "slim": "cl#eye:upper:slim",
                    "label": "eye_upper_slim",
                    "comment": "a subset of general classes related to specific cell types in the eye.",
                },
            ]
        ),
    )
    assert SlimManager.get_slim_list("Cell Ontology") == expected_get_slim_list


def test_get_slim_members():
    slim_list = ["blood_and_immune_upper_slim"]
    expected_get_slim_members = [
        "CL:0000037",
        "CL:0000038",
        "CL:0000097",
        "CL:0000145",
        "CL:0000232",
        "CL:0000233",
        "CL:0000235",
        "CL:0000236",
        "CL:0000547",
        "CL:0000556",
        "CL:0000558",
        "CL:0000576",
        "CL:0000647",
        "CL:0000762",
        "CL:0000765",
        "CL:0000767",
        "CL:0000771",
        "CL:0000775",
        "CL:0000784",
        "CL:0000786",
        "CL:0000789",
        "CL:0000798",
        "CL:0000816",
        "CL:0000837",
        "CL:0000842",
        "CL:0000889",
        "CL:0000990",
        "CL:0001065",
        "CL:0002031",
        "CL:0002032",
        "CL:0002087",
        "CL:0002420",
        "CL:0002679",
        "CL:0017005",
        "CL:0017006",
        "CL:4030029",
    ]

    get_slim_members = SlimManager.get_slim_members(slim_list)
    assert get_slim_members == expected_get_slim_members
