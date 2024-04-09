from models import FeaturesInput, PredictionOutput
from fastapi import FastAPI
import model_utils


app = FastAPI()


@app.post("/predict")
def prediction(fi: FeaturesInput):
    return PredictionOutput(nb_entree=model_utils.prediction(fi))
