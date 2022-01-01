"""Utilities."""

LANG_ID_LEN = 2


class ErrorMessage:
    """Server error messages."""

    no_such_lesson = "No such lesson: %{lesson_id}s"
    no_such_lesson_version = "No such lesson: %{lesson_id}s %{sequence_id}s"
    no_such_person = "No such person: %{person_id}s"


class HarperExc(Exception):
    """Harper-specific exceptions."""

    pass


def author_list(authors):
    """Convert list of author DB objects to JSON."""
    return [{"name": a.name, "email": a.email} for a in authors]


def term_list(terms):
    return [{"term": t.term, "url": t.url} for t in terms]
