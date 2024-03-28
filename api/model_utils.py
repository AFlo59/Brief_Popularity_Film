from joblib import load
import pandas as pd

def load_model(path='model.pkl'): # entrer le bon modèle 
    model = load(path)
    return model


# features (éventuellement modifiables) 
def prediction(model, data):
    
    """
    # bonnes features 
    df = pd.DataFrame(data, columns=['Url', 'TitreOriginal', 'Score', 'Genre',
                                    'Annee', 'Duree', 'Description', 'Acteurs', 'Pays']) 
    """

    # features fatctices pour tester  
    df = pd.DataFrame(data, columns=['SepalLength', 'SepalWidth', 'PetalLength', 'PetalWidth'])
    
    prediction = model.predict(df)
    return prediction[0]
