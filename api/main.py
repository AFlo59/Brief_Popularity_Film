import functools
from typing import List
from models import FeaturesInput, PredictionOutput
from fastapi import FastAPI
import model_utils
from db.database_mysql import engine
from sqlalchemy.sql import text


app = FastAPI()
conn = engine.connect()


@app.post("/predict")
def prediction(fi: FeaturesInput = None):
    if fi is None:
        query = conn.execute(text(""" select * from functionalities_filmscrap """))
        films = query.fetchall()

        for film in films:
            fi.year = film["year"]
            fi.director = film["director"]
            print(fi)
    else:
        return PredictionOutput(nb_entree=model_utils.prediction(fi))


@app.post("/batch_predict")
def batch_prediction():
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

        pred = PredictionOutput(nb_entree=model_utils.prediction(fi))
        preds.append({"id": film["id"], "title": film["title"], "pred": pred.nb_entree})

    films = sorted(preds, key=functools.cmp_to_key(comparer_classement))
    nb = 1
    for film in films:
        conn.execute(
            text(f""" update functionalities_filmscrap
                                    set classement = {nb} where id={film['id']}""")
        )
        conn.commit()

        nb = nb + 1
    # print(films)


def comparer_classement(film1, film2):
    return film2["pred"] - film1["pred"]
