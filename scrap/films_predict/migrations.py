from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class FilmModel(Base):
    __tablename__ = "films"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    director = Column(String, nullable=False)
    year = Column(Integer, default=-1)
    country = Column(String)
    duration = Column(Integer, default=-1)
    genre = Column(String)
    first_day = Column(Integer, default=-1)
    first_weekend = Column(Integer, default=-1)
    first_week = Column(Integer, default=-1)
    hebdo_rank = Column(Integer, default=-1)
    copies = Column(Integer, default=-1)

    time_created = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    time_updated = Column(
        DateTime(timezone=True), server_onupdate=func.now(), nullable=False
    )
