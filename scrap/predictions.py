import json
import pickle
from typing import List
import functools

import pandas as pd
from sklearn.pipeline import Pipeline
from pydantic import BaseModel
from db.database_mysql import engine
from sqlalchemy.sql import text
from joblib import load


# Modèle Pydantic pour la structure de donnée d'entrée
class FeaturesInput(BaseModel):
    year: int
    day: int
    month: int
    duration: int
    country: str
    genre: str
    director: str
    distributor: str
    casting: str


class PredictionOutput(BaseModel):
    nb_entree: float


conn = engine.connect()


def batch_prediction():
    query = conn.execute(
        text(
            """ SELECT  id,
                        YEAR(date) AS year, 
                        MONTH(date) AS month, 
                        DAY(date) AS day, 
                        duration, 
                        country, 
                        genre, 
                        director, 
                        distributor, 
                        casting 
                        FROM functionalities_filmscrap """
        )
    )
    films = query.mappings().all()

    for film in films:
        print(film["id"])
        pred = one_prediction(dict(film))
        conn.execute(
            text(f""" update functionalities_filmscrap
                                    set score_pred = {pred.nb_entree}
                                    where id='{film['id']}'""")
        )

        conn.commit()

    # print(preds)
    # films = sorted(preds, key=functools.cmp_to_key(comparer_classement))
    # nb = 1
    # for film in films:
    #     conn.execute(
    #         text(f""" update functionalities_filmscrap
    #                                 set classement = {nb}
    #                                 set score_pred = {film.pred}
    #                                 where id={film['id']}""")
    #     )
    #     conn.commit()

    #     nb = nb + 1
    # print(films)


def one_prediction(data: dict):
    casting = (
        eval(data["casting"]) if isinstance(data["casting"], str) else data["casting"]
    )
    distributor = (
        eval(data["distributor"])
        if isinstance(data["distributor"], str)
        else data["distributor"]
    )
    genre = eval(data["genre"]) if isinstance(data["genre"], str) else data["genre"]

    if isinstance(casting, list) is False:
        data["casting"] = [casting]
    if isinstance(distributor, list) is False:
        data["distributor"] = [distributor]
    if isinstance(genre, list) is False:
        data["genre"] = [genre]

    for key in data:
        data[key] = [data[key]]

    print(data)
    pipe_transform = load("_data_prediction/pipe_transform.pkl")
    model = load("_data_prediction/model.pkl")

    t = pipe_transform.transform(pd.DataFrame.from_dict(data))
    pred = PredictionOutput(nb_entree=model.predict(t))
    print(pred)
    return pred


def comparer_classement(film1, film2):
    return film2["pred"] - film1["pred"]


if __name__ == "__main__":
    data = {
        "year": 2024,
        "day": 10,
        "month": 4,
        "duration": 6120,
        "country": "france",
        "genre": ["comedie"],
        "director": '"florent bernard"',
        "distributor": ["nolita cinema", "tf1 studio", "apollo films"],
        "casting": ["charlotte gainsbourg", "jose garcia", "lily aubry"],
    }
    # {'id': 'tt27722491', 'year': 2024, 'month': 5, 'day': 1, 'duration': 5220, 'country': 'france', 'genre': '[]', 'director': '"nessim chikhaoui"', 'distributor': '["albertine productions", "prima vista"]', 'casting': '["fatima adoum", "corinne masiero", "mariama gueye"]'}
    # one_prediction(data)
    batch_prediction()
