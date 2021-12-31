"""Harper database interface."""

from sqlalchemy import Column, ForeignKey, Integer, Text, create_engine
from sqlalchemy.orm import declarative_base, relationship

from harper.util import HarperExc


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
    versions = relationship("LessonVersion")


class LessonVersion(DB.base):
    """Represent a specific version of a lesson."""

    __tablename__ = "lessonversion"
    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    lesson_id = Column(Integer, ForeignKey("lesson.id"))


class Person(DB.base):
    """Represent a person."""

    __tablename__ = "person"
    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    name = Column(Text, nullable=False)
    email = Column(Text, nullable=False)
