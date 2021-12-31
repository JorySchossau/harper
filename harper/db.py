"""Harper database interface."""

from sqlalchemy import Column, ForeignKey, Integer, Text, create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import declarative_base, relationship

from harper.util import HarperExc


# <https://docs.sqlalchemy.org/en/14/dialects/sqlite.html#sqlite-foreign-keys>
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
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


class Lesson(DB.base):
    """Represent a logical lesson."""

    __tablename__ = "lesson"
    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    versions = relationship(
        "LessonVersion", back_populates="lesson", cascade="all, delete"
    )


class LessonVersion(DB.base):
    """Represent a specific version of a lesson."""

    __tablename__ = "lessonversion"
    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    lesson_id = Column(Integer, ForeignKey("lesson.id"))
    lesson = relationship("Lesson", back_populates="versions")


class Person(DB.base):
    """Represent a person."""

    __tablename__ = "person"
    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    name = Column(Text, nullable=False)
    email = Column(Text, nullable=False)
