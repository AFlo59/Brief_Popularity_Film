from joblib import load
import pandas as pd

def load_model(path='model.pkl'): # entrer le bon modèle 
    model = load(path)
    return model


def prediction(model, data):

    # bonnes features 
    df = pd.DataFrame(data, columns=['Url', 'Titre', 'TitreOriginal', 'Score', 'Genre', 'Annee', 'Duree', 
                                    'Description', 'Acteurs', 'Public', 'Pays', 'LangueOriginal']) 
    
    prediction = model.predict(df)
    return prediction[0]


