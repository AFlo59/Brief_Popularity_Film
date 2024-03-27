from fastapi import FastAPI
from pydantic import BaseModel
import model_utils


app = FastAPI()
model = model_utils.load_model()


# Modèle Pydantic pour la structure de données d'entrée
class FeaturesInput(BaseModel):
    

class PredictionOutput(BaseModel):
    category: int


@app.post("/predict")
def prediction_root(feature_input: FeaturesInput):
    F1 = feature_input.
    F2 = feature_input.
    F3 = feature_input.
    F4 = feature_input.
    F5 = feature_input.
    F6 = feature_input.
    F7 = feature_input.
    F8 = feature_input.

    pred = model_utils.prediction(model, [[F1, F2, F3, F4, F5, F6, F7, F8]])

    return PredictionOutput(category=pred)
