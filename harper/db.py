"""Harper database interface."""

from dataclasses import dataclass
from datetime import datetime

from dataclasses_json import dataclass_json
from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
    UniqueConstraint,
    create_engine,
    event,
    func,
)
from sqlalchemy.engine import Engine
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.pool import StaticPool

from harper.util import LANG_ID_LEN, HarperExc


def timestamp():
    """Return current time."""
    result = datetime.utcnow()
    return result


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
            DB.engine = create_engine(
                "sqlite://",
                connect_args={"check_same_thread": False},
                poolclass=StaticPool,
            )
            DB.base.metadata.drop_all(DB.engine)
            DB.base.metadata.create_all(DB.engine)
            return DB.engine
        else:
            raise HarperExc(f"Unknown database back-end '{name}'")

    @staticmethod
    def get_current_lesson_version(session, lesson_id):
        """Get the latest version."""
        subquery = (
            session.query(func.max(LessonVersion.id))
            .filter(LessonVersion.lesson_id == lesson_id)
            .scalar_subquery()
        )
        query = session.query(LessonVersion).filter(
            LessonVersion.lesson_id == lesson_id, LessonVersion.id == subquery
        )
        return query.one()

    @staticmethod
    def build_lesson_version(session, **kwargs):
        """Add next sequence ID value to lession version."""
        max_sequence_id = (
            session.query(func.max(LessonVersion.sequence_id))
            .filter(LessonVersion.lesson_id == kwargs["lesson_id"])
            .scalar()
        )
        sequence_id = 1 if (max_sequence_id is None) else (max_sequence_id + 1)
        return LessonVersion(sequence_id=sequence_id, **kwargs)


@dataclass_json
@dataclass
class StandardFields:
    """Common definitions for all tables."""

    id: int
    created_at: datetime

    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=timestamp)


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
    Column("term_id", ForeignKey("term.id"), nullable=False, primary_key=True),
    Column(
        "lesson_version_id",
        ForeignKey("lesson_version.id"),
        nullable=False,
        primary_key=True,
    ),
)


@dataclass
class Lesson(DB.base, StandardFields):
    """Represent a logical lesson."""

    language: str

    __tablename__ = "lesson"
    language = Column(String(LANG_ID_LEN), nullable=False)
    versions = relationship(
        "LessonVersion", back_populates="lesson", cascade="all, delete"
    )


@dataclass
class LessonVersion(DB.base, StandardFields):
    """Represent a specific version of a lesson."""

    lesson_id: int
    sequence_id: int
    title: str
    url: str
    abstract: str
    version: str
    license: str

    __tablename__ = "lesson_version"
    lesson_id = Column(Integer, ForeignKey("lesson.id"))
    sequence_id = Column(Integer, nullable=False)
    title = Column(Text, nullable=False)
    url = Column(Text, nullable=False)
    abstract = Column(Text, nullable=False)
    version = Column(Text, nullable=False)
    license = Column(Text, nullable=False)
    lesson = relationship("Lesson", back_populates="versions")
    authors = relationship(
        "Person", secondary="lesson_version_author", back_populates="lesson_versions"
    )
    terms = relationship(
        "Term", secondary="lesson_version_term", back_populates="lesson_versions"
    )


@dataclass
class Term(DB.base, StandardFields):
    """Represent a term used as a pre- or post-requisite."""

    language: str
    term: str
    url: str

    __tablename__ = "term"
    __table_args__ = (
        UniqueConstraint("language", "term", name="language_term_unique"),
    )
    language = Column(String(LANG_ID_LEN), nullable=False)
    term = Column(Text, nullable=False)
    url = Column(Text, nullable=False)
    lesson_versions = relationship(
        "LessonVersion", secondary="lesson_version_term", back_populates="terms"
    )


@dataclass
class Person(DB.base, StandardFields):
    """Represent a person."""

    name: str
    email: str

    __tablename__ = "person"
    name = Column(Text, nullable=False)
    email = Column(Text, nullable=False)
    lesson_versions = relationship(
        "LessonVersion", secondary="lesson_version_author", back_populates="authors"
    )
