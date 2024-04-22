import pandas as pd
from modelisation.functions import load_file


def drop_after_converter(df):
    return df.drop(
        columns=[
            "director",
            "casting",
            "distributor",
            "country",
            "month",
            "day",
            "year",
        ]
    )


def convert_entrees_year(df, column):
    scores = load_file("year_scores")

    val = []
    for index, row in df.iterrows():
        try:
            found = scores.loc[scores[column] == df.iloc[index][column]]
            val.append(found.iloc[0]["year_combined_score"])
        except Exception:
            val.append(0)

    df["year_combined_score"] = pd.Series(val)

    return df


def convert_country(df, column):
    scores = load_file("country_scores")

    val = []
    for index, row in df.iterrows():
        try:
            found = scores.loc[scores[column] == df.iloc[index][column]]
            val.append(found.iloc[0]["country_combined_score"])
        except Exception:
            val.append(0)

    df["country_combined_score"] = pd.Series(val)

    return df


def convert_director(df, column):
    scores = load_file("director_scores")
    mean_score = scores["director_combined_score"].median()
    val = []
    for index, row in df.iterrows():
        try:
            found = scores.loc[scores[column] == df.iloc[index][column]]
            val.append(found.iloc[0]["director_combined_score"])
        except Exception:
            val.append(mean_score)

    df["director_combined_score"] = pd.Series(val)
    return df


def convert_actor(df, column):
    scores = load_file("actor_scores")

    # Calculer la médiane des scores des acteurs à utiliser comme valeur par défaut
    mean_score = scores["actor_combined_score"].median()

    # Liste pour stocker les scores calculés
    val = []
    for index, row in df.iterrows():
        actors_scores = []
        df_actors = df.iloc[index][
            column
        ]  # Assurez-vous que df_actors est une liste d'acteurs
        try:
            for actor in df_actors:
                try:
                    found = scores[scores["actor"] == actor]
                    if not found.empty:
                        actors_scores.append(found.iloc[0]["actor_combined_score"])
                except Exception:
                    pass
        except Exception:
            pass

        if actors_scores:  # Si la liste n'est pas vide, calculer la moyenne
            val.append(sum(actors_scores) / len(actors_scores))
        else:  # Si aucun acteur trouvé, utiliser la médiane des scores comme valeur par défaut
            val.append(mean_score)

    # Ajouter les scores calculés au DataFrame
    df["actor_combined_score"] = pd.Series(val)
    return df


def convert_distributor(df, column):
    scores = load_file("distributor_scores")

    # Calculer la médiane des scores des distributeurs à utiliser comme valeur par défaut
    mean_score = scores["distributor_combined_score"].median()

    # Liste pour stocker les scores calculés
    val = []
    for index, row in df.iterrows():
        distributors_scores = []
        df_distributors = df.iloc[index][
            column
        ]  # Assurez-vous que df_distributors est une liste de distributeurs
        for distributor in df_distributors:
            found = scores[scores["distributor"] == distributor]
            if not found.empty:
                distributors_scores.append(found.iloc[0]["distributor_combined_score"])

        if distributors_scores:  # Si la liste n'est pas vide, calculer la moyenne
            val.append(sum(distributors_scores) / len(distributors_scores))
        else:  # Si aucun distributeur trouvé, utiliser la médiane des scores comme valeur par défaut
            val.append(mean_score)

    # Ajouter les scores calculés au DataFrame
    df["distributor_combined_score"] = pd.Series(val)
    return df
