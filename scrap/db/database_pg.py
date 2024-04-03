from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from utils.environment import get_env
import urllib.parse

DB_NAME = get_env("FILM_DB")
DB_USER = get_env("FILM_USER")
DB_IP = get_env("IP_DB")
DB_PASSWORD = urllib.parse.quote_plus(get_env("FILM_PWD"))

SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_IP}/{DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionMaker = sessionmaker(autocommit=False, autoflush=False, bind=engine)

session = SessionMaker()
