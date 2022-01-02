"""Testing utilities (not fixtures)."""


def dict_list_match(major, expected, actual):
    expected = {entry[major]:entry for entry in expected}
    actual = {entry[major]:entry for entry in actual}
    if set(expected.keys()) != set(actual.keys()):
        return False
    for (outer, expected_item) in expected.items():
        for inner in expected_item:
            if actual[outer][inner] != expected_item[inner]:
                return False
    return True


def error_match(actual, expected):
    """Check that an actual error message matches a template."""
    return actual.split(":")[0] == expected.split(":")[0]
