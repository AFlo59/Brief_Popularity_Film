from sqlalchemy import Column, String, text
from sqlalchemy.dialects.mysql import (
    TIMESTAMP,
    INTEGER,
    FLOAT,
    TEXT,
    JSON,
    BIGINT,
    DATE,
)

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class FilmModel(Base):
    __tablename__ = "films_jp"
    mysql_engine = "InnoDB"
    mysql_charset = "utf8mb4"

    id = Column(String(255), primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    original_title = Column(String(255))
    date = Column(DATE)
    director = Column(String(255), nullable=False)
    raw_title = Column(String(255), nullable=False)
    raw_director = Column(String(255), nullable=False)
    url_jp = Column(String(255), nullable=False)
    year = Column(INTEGER(4), default=-1)
    country = Column(String(100))
    duration = Column(INTEGER(6), default=-1)
    genre = Column(String(100))
    first_day = Column(INTEGER(9), default=-1)
    first_weekend = Column(INTEGER(9), default=-1)
    first_week = Column(INTEGER(9), default=-1)
    hebdo_rank = Column(INTEGER(9), default=-1)
    total_spectator = Column(INTEGER(9), default=-1)
    copies = Column(INTEGER(6), default=-1)
    scraped = Column(INTEGER(1), default=0)

    time_created = Column(
        TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), nullable=False
    )
    time_updated = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        onupdate=func.now(),
        nullable=False,
    )


class FilmImdbModel(Base):
    __tablename__ = "films_imdb"
    mysql_engine = "InnoDB"
    mysql_charset = "utf8mb4"

    id = Column(String(255), primary_key=True, index=True)
    id_jp = Column(String(255), nullable=False)
    url = Column(String(255), nullable=False)
    title = Column(String(255), nullable=True)
    original_title = Column(String(255), nullable=True)
    date = Column(DATE)
    director = Column(JSON)
    synopsis = Column(TEXT)
    distributor = Column(JSON)
    casting = Column(JSON)
    rating_press = Column(FLOAT)
    rating_public = Column(FLOAT)
    award = Column(INTEGER)
    budget = Column(BIGINT)
    lang = Column(JSON)
    genre = Column(JSON)
    genre_raw = Column(JSON)

    time_created = Column(
        TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), nullable=False
    )
    time_updated = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        onupdate=func.now(),
        nullable=False,
    )


class FilmAlloModel(Base):
    __tablename__ = "films_allo"
    mysql_engine = "InnoDB"
    mysql_charset = "utf8mb4"

    id = Column(String(255), primary_key=True, index=True)
    id_jp = Column(String(255), nullable=False)
    url_allo = Column(String(255), nullable=False)
    director_allo = Column(JSON)
    year_allo = Column(INTEGER(4), default=-1)
    synopsis = Column(TEXT)
    distributor = Column(String(100))
    casting = Column(JSON)
    rating_press = Column(FLOAT)
    rating_public = Column(FLOAT)
    award = Column(INTEGER)
    budget = Column(BIGINT)
    lang = Column(JSON)
    visa = Column(INTEGER)

    time_created = Column(
        TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), nullable=False
    )
    time_updated = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        onupdate=func.now(),
        nullable=False,
    )


class FilmSortieModel(Base):
    __tablename__ = "functionalities_filmscrap"
    mysql_engine = "InnoDB"
    mysql_charset = "utf8mb4"

    id = Column(String(255), primary_key=True, index=True)
    url = Column(String(255))
    classement = Column(BIGINT)
    title = Column(String(255))
    original_title = Column(String(255))
    date = Column(DATE)
    director = Column(JSON)
    synopsis = Column(TEXT)
    distributor = Column(JSON)
    casting = Column(JSON)
    rating_press = Column(FLOAT)
    rating_public = Column(FLOAT)
    award = Column(INTEGER)
    budget = Column(BIGINT)
    lang = Column(JSON)
    thumbnail = Column(String(255))
    copies = Column(BIGINT)
    score_pred = Column(FLOAT)
    duration = Column(INTEGER)
    genre = Column(JSON)
    genre_raw = Column(JSON)
    country = Column(String(100))

    time_created = Column(
        TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), nullable=False
    )
    time_updated = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        onupdate=func.now(),
        nullable=False,
    )
