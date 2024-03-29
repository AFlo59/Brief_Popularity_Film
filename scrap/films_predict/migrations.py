from sqlalchemy import Column, String, text, TIMESTAMP
from sqlalchemy.dialects.mysql import TIMESTAMP, INTEGER

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class FilmModel(Base):
    __tablename__ = "films"
    mysql_engine = "InnoDB"
    mysql_charset = "utf8mb4"

    id = Column(String(255), primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    director = Column(String(255), nullable=False)
    year = Column(INTEGER(4), default=-1)
    country = Column(String(100))
    duration = Column(INTEGER(6), default=-1)
    genre = Column(String(100))
    first_day = Column(INTEGER(6), default=-1)
    first_weekend = Column(INTEGER(6), default=-1)
    first_week = Column(INTEGER(6), default=-1)
    hebdo_rank = Column(INTEGER(6), default=-1)
    copies = Column(INTEGER(6), default=-1)

    time_created = Column(
        TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), nullable=False
    )
    time_updated = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        onupdate=func.now(),
        nullable=False,
    )
