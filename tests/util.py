"""Testing utilities (not fixtures)."""


def error_match(actual, expected):
    """Check that an actual error message matches a template."""
    return actual.split(":")[0] == expected.split(":")[0]
