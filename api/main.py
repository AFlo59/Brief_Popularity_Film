from fastapi import FastAPI
from pydantic import BaseModel
import model_utils


app = FastAPI()
model = model_utils.load_model()


# Modèle Pydantic pour la structure de donnée d'entrée
class FeaturesInput(BaseModel):
    Url: int
    Titre: str
    TitreOriginal: str
    Score: float
    Genre: str
    Annee: int
    Duree: float    
    Description: str
    Acteurs: str
    Public: str
    Pays: str
    LangueOrigine: str

class PredictionOutput(BaseModel):
    category: int


@app.post("/predict")
def prediction_root(feature_input: FeaturesInput):
    F1 = feature_input.Url
    F2 = feature_input.Titre
    F3 = feature_input.TitreOriginal
    F4 = feature_input.Score
    F5 = feature_input.Genre
    F6 = feature_input.Annee
    F7 = feature_input.Duree
    F8 = feature_input.Description
    F9 = feature_input.Acteurs
    F10 = feature_input.Public
    F11 = feature_input.Pays 
    F12 = feature_input.LangueOrigine
    
    pred = model_utils.prediction(model, [[F1, F2, F3, F4, F5, F6, F7, F8, F9, F10, F11, F12]])

    return PredictionOutput(category=pred)
