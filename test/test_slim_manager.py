from src.pandasaurus.slim_manager import SlimManager


def test_find_slim_list():
    pass


def test_show_slim_content():
    slim_list = ["blood_and_immune_upper_slim"]
    expected_show_slim_content = [
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

    show_slim_content = SlimManager.get_slim_members(slim_list)
    assert show_slim_content == expected_show_slim_content
