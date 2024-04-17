from typing import List
import functools

from sklearn.pipeline import Pipeline
from pydantic import BaseModel
from db.database_mysql import engine
from sqlalchemy.sql import text
from joblib import load


# Modèle Pydantic pour la structure de donnée d'entrée
class FeaturesInput(BaseModel):
    year: int
    director: str
    country: str
    duration: int
    genre: str
    copies: int
    rating_press: float
    first_day: int
    budget: int
    distributor: str
    casting: List


class PredictionOutput(BaseModel):
    nb_entree: int


conn = engine.connect()


def load_model(path="model.pickle") -> Pipeline:  # entrer le bon modèle
    model = load(path)
    return model


def batch_prediction():
    model = load_model()
    query = conn.execute(text(""" select * from functionalities_filmscrap """))
    films = query.mappings().all()

    preds = []

    for film in films:
        casting = eval(film["casting"])

        if type(casting) is not List:
            casting = [casting]

        fi = FeaturesInput(
            year=2024,
            director=film["director_raw"] if film["director_raw"] is not None else "",
            country="etatsunis",
            duration=film["duration"],
            genre=film["genre"] if film["genre"] is not None else "",
            copies=600,
            rating_press=film["rating_press"],
            first_day=100000,
            budget=1000000,
            distributor=film["distributor"],
            casting=casting,
        )

        pred = PredictionOutput(nb_entree=model.predict(fi))
        preds.append({"id": film["id"], "title": film["title"], "pred": pred.nb_entree})

    films = sorted(preds, key=functools.cmp_to_key(comparer_classement))
    nb = 1
    for film in films:
        conn.execute(
            text(f""" update functionalities_filmscrap
                                    set classement = {nb}
                                    set score_pred = {film.pred}
                                    where id={film['id']}""")
        )
        conn.commit()

        nb = nb + 1
    # print(films)


def comparer_classement(film1, film2):
    return film2["pred"] - film1["pred"]
