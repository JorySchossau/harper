"""Utilities."""

from functools import wraps

from fastapi import HTTPException


LANG_ID_LEN = 2


class ErrorMessage:
    """Server error messages."""

    no_such_lesson = "No such lesson: %{lesson_id}s"
    no_such_lesson_version = "No such lesson: %{lesson_id}s %{sequence_id}s"
    no_such_person = "No such person: %{person_id}s"


class HarperExc(Exception):
    """Harper-specific exceptions."""

    def __init__(self, message, code=None):
        """Construct exception with optional HTTP status code."""
        self.message = message
        self.code = code


def harper_exc(original):
    """Convert Harper exceptions to HTTP exceptions."""
    # https://stackoverflow.com/questions/64497615/how-to-add-a-custom-decorator-to-a-fastapi-route
    @wraps(original)
    async def wrapped(*args, **kwargs):
        try:
            return await original(*args, **kwargs)
        except HarperExc as exc:
            raise HTTPException(status_code=exc.code, detail=exc.message)
    return wrapped


def author_list(authors):
    """Convert list of author DB objects to JSON."""
    return [{"name": a.name, "email": a.email} for a in authors]


def term_list(terms):
    """Convert list of term DB objects to JSON."""
    return [{"term": t.term, "url": t.url} for t in terms]


def get_db_schema(engine):
    """Find the tables and columns in the database.

    Args:
        engine: SQLAlchemy database connection engine.

    Returns:
        A dict-of-sets with table names as keys and column names as values.
    """
    result = {}
    inspector = inspect(engine)
    for table_name in inspector.get_table_names():
        result[table_name] = set()
        for column in inspector.get_columns(table_name):
            result[table_name].add(column["name"])
    return result


def get_model_schema(metadata):
    """Find the tables and columns in the SQLAlchemy model.

    Args:
        metadata: SQLAlchemy metadata structure.

    Returns:
        A dict-of-sets with table names as keys and column names as values.
    """
    result = {}
    for table in metadata.sorted_tables:
        result[table.name] = set()
        for column in table.columns:
            result[table.name].add(column.name)
    return result
