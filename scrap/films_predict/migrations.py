from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Float,
    Boolean,
    text,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()


class FilmModel(Base):
    __tablename__ = "films"
    id = Column(Integer, primary_key=True, index=True)

    title = Column(String)
    director = Column(String)
    year = Column(Integer)
    country = Column(String)
    duration = Column(Integer)
    genre = Column(String)
    first_day = Column(Integer)
    first_weekend = Column(Integer)
    first_week = Column(Integer)
    hebdo_rank = Column(Integer)
    copies = Column(Integer)

    time_created = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    time_updated = Column(DateTime(timezone=True), onupdate=func.now(), nullable=False)
