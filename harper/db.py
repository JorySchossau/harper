"""Harper database interface."""

from datetime import datetime

from sqlalchemy import (
    TIMESTAMP,
    Column,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
    UniqueConstraint,
    create_engine,
    event,
)
from sqlalchemy.engine import Engine
from sqlalchemy.orm import declarative_base, relationship

from harper.util import HarperExc, LANG_ID_LEN


# <https://docs.sqlalchemy.org/en/14/dialects/sqlite.html#sqlite-foreign-keys>
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """Ensure that cascading deletes work for SQLite."""
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


class DB:
    """Connect to database."""

    # SQLAlchemy base class.
    base = declarative_base()

    # Database connection engine (assigned during configuration).
    engine = None

    @staticmethod
    def configure(name):
        """Configure the back end."""
        if name == "sqlite":
            DB.engine = create_engine("sqlite+pysqlite:///:memory:")
            DB.base.metadata.create_all(DB.engine)
            return DB.engine
        else:
            raise HarperExc(f"Unknown database back-end '{name}'")


class StandardFields:
    """Common definitions for all tables."""

    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.utcnow)


# Link lesson versions to authors.
lesson_version_author = Table(
    "lesson_version_author",
    DB.base.metadata,
    Column("author_id", ForeignKey("person.id"), primary_key=True),
    Column("lesson_version_id", ForeignKey("lesson_version.id"), primary_key=True),
)


# Link lesson versions to terms.
lesson_version_term = Table(
    "lesson_version_term",
    DB.base.metadata,
    Column("term_id", ForeignKey("term.id"), primary_key=True),
    Column("lesson_version_id", ForeignKey("lesson_version.id"), primary_key=True),
)


class Lesson(DB.base, StandardFields):
    """Represent a logical lesson."""

    __tablename__ = "lesson"
    versions = relationship(
        "LessonVersion", back_populates="lesson", cascade="all, delete"
    )


class LessonVersion(DB.base, StandardFields):
    """Represent a specific version of a lesson."""

    __tablename__ = "lesson_version"
    lesson_id = Column(Integer, ForeignKey("lesson.id"))
    lesson = relationship("Lesson", back_populates="versions")
    authors = relationship(
        "Person", secondary=lesson_version_author, back_populates="lesson_versions"
    )
    terms = relationship(
        "Term", secondary=lesson_version_term, back_populates="lesson_versions"
    )


class Term(DB.base, StandardFields):
    """Represent a term used as a pre- or post-requisite."""

    __tablename__ = "term"
    __table_args__ = (
        UniqueConstraint("language", "term", name="language_term_unique"),
    )
    language = Column(String(LANG_ID_LEN), nullable=False)
    term = Column(Text, nullable=False)
    url = Column(Text, nullable=False)
    lesson_versions = relationship(
        "LessonVersion", secondary=lesson_version_term, back_populates="terms"
    )


class Person(DB.base, StandardFields):
    """Represent a person."""

    __tablename__ = "person"
    name = Column(Text, nullable=False)
    email = Column(Text, nullable=False)
    lesson_versions = relationship(
        "LessonVersion", secondary=lesson_version_author, back_populates="authors"
    )
