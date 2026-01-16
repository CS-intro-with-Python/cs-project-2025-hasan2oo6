from app import parse_groups

def test_parse_groups_valid():
    groups = parse_groups("2 800 1200 any dp")
    assert len(groups) == 1
    assert groups[0]["count"] == 2

def test_parse_groups_invalid():
    try:
        parse_groups("wrong input")
        assert False
    except ValueError:
        assert True
