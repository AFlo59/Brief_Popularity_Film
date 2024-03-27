from joblib import load
import pandas as pd

def load_model(path=''): # entrer modèle ou modèle factice
    model = load(path)
    return model

def prediction(model, data):
    df = pd.DataFrame(data, columns=[]) # entrer features
    prediction = model.predict(df)
    return prediction[0]