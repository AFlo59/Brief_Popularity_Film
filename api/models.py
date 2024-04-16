from typing import List
from pydantic import BaseModel


# Modèle Pydantic pour la structure de donnée d'entrée
class FeaturesInput(BaseModel):
    # year    director    country    duration    genre    copies    rating_press    first_day    budget    classification_acteurs    distributor
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
