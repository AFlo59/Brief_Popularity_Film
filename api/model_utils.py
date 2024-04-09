from models import FeaturesInput
from joblib import load
from sklearn.pipeline import Pipeline
import json
import pandas as pd


def load_model(path="model.pickle") -> Pipeline:  # entrer le bon modèle
    model = load(path)
    return model


def classifier_acteurs(acteurs):
    f = open("acteurs.json")
    acteurs = json.load(f)

    for acteur in acteurs:
        if acteur in acteurs["acteurs_tres_connus"] or acteurs["acteurs_moins_connus"]:
            return 1
        # elif acteur in acteurs_moins_connus:
        #     return 2
        else:
            return 2


def classifier_directors(director):
    return 1
    # f = open("acteurs.json")
    # acteurs = json.load(f)

    # for acteur in acteurs:
    #     if acteur in acteurs["acteurs_tres_connus"] or acteurs["acteurs_moins_connus"]:
    #         return 1
    #     # elif acteur in acteurs_moins_connus:
    #     #     return 2
    #     else:
    #         return 2


def classifier_distributor(distributor):
    return 1
    # f = open("acteurs.json")
    # acteurs = json.load(f)

    # for acteur in acteurs:
    #     if acteur in acteurs["acteurs_tres_connus"] or acteurs["acteurs_moins_connus"]:
    #         return 1
    #     # elif acteur in acteurs_moins_connus:
    #     #     return 2
    #     else:
    #         return 2


# {
#   "year": 2023,
#   "director": "Greta Gerwig",
#   "country": "etatsunis",
#   "duration": 7200,
#   "genre": "comedie",
#   "copies": 665,
#   "rating_press": 4,
#   "first_day": 359889,
#   "budget": 100000000,
#   "distributor": "Greta Gerwig",
#   "casting": [
#     "Margot Robbie", "Ryan Gosling", "Issa Rae"
#   ]
# }


def prediction(data: FeaturesInput):
    model = load_model()
    print(model)
    classification_acteurs = classifier_acteurs(data.casting)
    classification_director = classifier_directors(data.director)
    classification_distributor = classifier_distributor(data.distributor)

    values = {}
    print(data.__dict__)
    for key, value in data.__dict__.items():
        if key != "casting":
            values[key] = [value]

    values["classification_acteurs"] = classification_acteurs
    values["director"] = classification_director
    values["distributor"] = classification_distributor
    df = pd.DataFrame.from_dict(values)

    prediction = model.predict(df)
    return prediction[0]
