import json
from joblib import dump, load
from vacances_scolaires_france import SchoolHolidayDates
import datetime
import pandas as pd


def classify_entrees_year(df, column):
    # print(type(valeur))
    for index, valeur in df[column].items():
        if valeur == 1986:
            df.at[index, "entree_annee"] = 168.1
        elif valeur == 1992:
            df.at[index, "entree_annee"] = 116.0
        elif valeur == 1993:
            df.at[index, "entree_annee"] = 132.7
        elif valeur == 1994:
            df.at[index, "entree_annee"] = 124.4
        elif valeur == 1995:
            df.at[index, "entree_annee"] = 130.2
        elif valeur == 1996:
            df.at[index, "entree_annee"] = 136.7
        elif valeur == 1997:
            df.at[index, "entree_annee"] = 149.3
        elif valeur == 1998:
            df.at[index, "entree_annee"] = 170.6
        elif valeur == 1999:
            df.at[index, "entree_annee"] = 153.6
        elif valeur == 2000:
            df.at[index, "entree_annee"] = 165.8
        elif valeur == 2001:
            df.at[index, "entree_annee"] = 187.5
        elif valeur == 2002:
            df.at[index, "entree_annee"] = 184.4
        elif valeur == 2003:
            df.at[index, "entree_annee"] = 173.5
        elif valeur == 2004:
            df.at[index, "entree_annee"] = 195.8
        elif valeur == 2005:
            df.at[index, "entree_annee"] = 175.6
        elif valeur == 2006:
            df.at[index, "entree_annee"] = 188.8
        elif valeur == 2007:
            df.at[index, "entree_annee"] = 178.5
        elif valeur == 2008:
            df.at[index, "entree_annee"] = 190.3
        elif valeur == 2009:
            df.at[index, "entree_annee"] = 201.6
        elif valeur == 2010:
            df.at[index, "entree_annee"] = 207.1
        elif valeur == 2011:
            df.at[index, "entree_annee"] = 217.2
        elif valeur == 2012:
            df.at[index, "entree_annee"] = 203.6
        elif valeur == 2013:
            df.at[index, "entree_annee"] = 193.7
        elif valeur == 2014:
            df.at[index, "entree_annee"] = 209.1
        elif valeur == 2015:
            df.at[index, "entree_annee"] = 205.4
        elif valeur == 2016:
            df.at[index, "entree_annee"] = 213.2
        elif valeur == 2017:
            df.at[index, "entree_annee"] = 209.4
        elif valeur == 2018:
            df.at[index, "entree_annee"] = 201.2
        elif valeur == 2019:
            df.at[index, "entree_annee"] = 213.2
        elif valeur == 2020:
            df.at[index, "entree_annee"] = 65.3
        elif valeur == 2021:
            df.at[index, "entree_annee"] = 95.5
        elif valeur == 2022:
            df.at[index, "entree_annee"] = 152.0
        elif valeur == 2023 or 2024:
            df.at[index, "entree_annee"] = 180.8
        else:
            df.at[index, "entree_annee"] = 150

    return df


def classify_season(df, column):
    for index, valeur in df[column].items():
        if valeur == 12 or valeur == 1 or valeur == 2:
            df.at[index, "season"] = "winter"
        elif valeur == 3 or valeur == 4 or valeur == 5:
            df.at[index, "season"] = "spring"
        elif valeur == 6 or valeur == 7 or valeur == 8:
            df.at[index, "season"] = "summer"
        elif valeur == 9 or valeur == 10 or valeur == 11:
            df.at[index, "season"] = "autumn"

    return df


def classify_month_name(df, column):
    for index, valeur in df[column].items():
        if valeur == 12:
            df.at[index, "month_name"] = "december"
        elif valeur == 11:
            df.at[index, "month_name"] = "novembre"
        elif valeur == 10:
            df.at[index, "month_name"] = "october"
        elif valeur == 9:
            df.at[index, "month_name"] = "september"
        elif valeur == 8:
            df.at[index, "month_name"] = "august"
        elif valeur == 7:
            df.at[index, "month_name"] = "july"
        elif valeur == 6:
            df.at[index, "month_name"] = "june"
        elif valeur == 5:
            df.at[index, "month_name"] = "may"
        elif valeur == 4:
            df.at[index, "month_name"] = "april"
        elif valeur == 3:
            df.at[index, "month_name"] = "march"
        elif valeur == 2:
            df.at[index, "month_name"] = "february"
        elif valeur == 1:
            df.at[index, "month_name"] = "january"
    return df


def is_holiday(df):
    holiday_dates = SchoolHolidayDates()

    df["is_holiday"] = df.apply(
        lambda row: holiday_dates.is_holiday_for_zone(
            datetime.date(row["year"], row["month"], row["day"]), "B"
        ),
        axis=1,
    )
    df["is_holiday"] = df["is_holiday"].astype(int)
    return df


# def nettoyer_genre(df):
#     for index, row in df.iterrows():
#         print(df.iloc[index]['genre'].at[0])
#         try:
#             df.iloc[index]['genre'] =  df.iloc[index]['genre'][0]
#         except Exception:
#             pass

#     return df


def nettoyer_genre(df):
    return df["genre"].apply(lambda x: json.loads(x)[0] if x is not None else x)
    # df["genre"] = df["genre"].apply(lambda x: x.split()[0] if x else None)
    # df["genre"] = df["genre"].str.replace('"', "")
    # df["genre"] = df["genre"].str.replace("[", "")
    # df["genre"] = df["genre"].str.replace("]", "")
    # df["genre"] = df["genre"].str.replace(",", "")
    # return df


# ---------------------------------------------------


def calculate_director_scores(df):
    # 1. Fréquence de réalisation
    frequency = df["director"].value_counts()
    # 2. Moyenne des spectateurs totaux
    avg_total_spectators = df.groupby("director")["total_spectator"].mean()
    # 3. Moyenne de la première semaine
    avg_first_week = df.groupby("director")["first_week"].mean()
    # 4. Moyenne inversée du classement hebdomadaire
    avg_inv_hebdo_rank = 1 / df.groupby("director")["hebdo_rank"].mean()
    # 5. Moyenne des évaluations de la presse
    avg_rating_press = df.groupby("director")["rating_press"].mean()
    # 6. Moyenne des récompenses
    avg_award = df.groupby("director")["award"].mean()
    # 7. Rendement (total_spectator / budget)
    performance = (
        df.groupby("director")["total_spectator"].sum()
        / df.groupby("director")["budget"].sum()
    )

    # Compilation des scores dans un DataFrame
    director_scores = pd.DataFrame(
        {
            "frequency": frequency,
            "avg_total_spectators": avg_total_spectators,
            "avg_first_week": avg_first_week,
            "avg_inv_hebdo_rank": avg_inv_hebdo_rank,
            "avg_rating_press": avg_rating_press,
            "avg_award": avg_award,
            "performance": performance,
        }
    )

    # Normalisation des scores
    max_values = director_scores.max()
    normalized_scores = director_scores / max_values

    # Combinaison des scores normalisés
    normalized_scores["director_combined_score"] = normalized_scores.mean(axis=1)

    # Joindre avec le DataFrame principal
    df = df.join(normalized_scores["director_combined_score"], on="director")
    save_files(df[["director", "director_combined_score"]], "director_scores")
    return df


def calculate_distributor_scores(df):
    f_distributors = pd.DataFrame(
        df["distributor"].str.strip("[]").str.split(",").explode().unique(),
        columns=["distributors"],
    )
    distributor_counts = df["distributor"].str.strip("[]").str.split(",").explode().value_counts()
    # Convertir les acteurs en listes à partir des chaînes de caractères
    df["distributor_list"] = df["distributor"].str.strip("[]s").str.split(",")

    # Exploder cette colonne pour avoir une ligne par acteur par film
    expanded_df = df.explode("distributor_list")

    # Calculer la moyenne des évaluations de la presse pour chaque acteur
    avg_rating_by_distributor = expanded_df.groupby("distributor_list")["rating_press"].mean()
    performance_by_distributor = expanded_df.groupby("distributor_list").apply(
        lambda x: (x["total_spectator"].sum() / x["budget"].sum())
        if x["budget"].sum() > 0
        else 0
    )

    # Création d'un DataFrame pour les scores
    scores = pd.DataFrame(
        {
            "frequency": distributor_counts,
            "avg_rating_press": avg_rating_by_distributor,
            "performance": performance_by_distributor,
        }
    )

    # Normalisation des scores (chaque colonne sera divisée par sa valeur maximale)
    normalized_scores = scores.apply(lambda x: x / x.max())

    # Calcul du score combiné
    normalized_scores["distributor_combined_score"] = normalized_scores.mean(axis=1)
    f_distributors = f_distributors.join(normalized_scores["distributor_combined_score"], on="distributors")
    f_distributors["distributor"] = f_distributors["distributors"].str.replace('"', "")
    save_files(f_distributors[["distributor", "distributor_combined_score"]], "distributor_scores")
    return df



def calculate_actor_scores(df):
    f_acteurs = pd.DataFrame(
        df["casting"].str.strip("[]").str.split(",").explode().unique(),
        columns=["actor"],
    )
    actor_counts = df["casting"].str.strip("[]").str.split(",").explode().value_counts()
    # Convertir les acteurs en listes à partir des chaînes de caractères
    df["actor_list"] = df["casting"].str.strip("[]s").str.split(",")

    # Exploder cette colonne pour avoir une ligne par acteur par film
    expanded_df = df.explode("actor_list")

    # Calculer la moyenne des évaluations de la presse pour chaque acteur
    avg_rating_by_actor = expanded_df.groupby("actor_list")["rating_press"].mean()
    performance_by_actor = expanded_df.groupby("actor_list").apply(
        lambda x: (x["total_spectator"].sum() / x["budget"].sum())
        if x["budget"].sum() > 0
        else 0
    )

    # Création d'un DataFrame pour les scores
    scores = pd.DataFrame(
        {
            "frequency": actor_counts,
            "avg_rating_press": avg_rating_by_actor,
            "performance": performance_by_actor,
        }
    )

    # Normalisation des scores (chaque colonne sera divisée par sa valeur maximale)
    normalized_scores = scores.apply(lambda x: x / x.max())

    # Calcul du score combiné
    normalized_scores["actor_combined_score"] = normalized_scores.mean(axis=1)
    f_acteurs = f_acteurs.join(normalized_scores["actor_combined_score"], on="actor")
    f_acteurs["actor"] = f_acteurs["actor"].str.replace('"', "")
    save_files(f_acteurs[["actor", "actor_combined_score"]], "actor_scores")
    return df


def calculate_year_scores(df):
    # 1. Fréquence de distribution
    frequency = df["year"].value_counts()
    # 2. Moyenne des spectateurs totaux
    avg_total_spectators = df.groupby("year")["total_spectator"].mean()
    # 3. Moyenne de la première semaine
    avg_first_week = df.groupby("year")["first_week"].mean()
    # 4. Moyenne du nombre de copies
    avg_copies = df.groupby("year")["copies"].mean()

    # Compilation des scores dans un DataFrame
    year_scores = pd.DataFrame(
        {
            "frequency": frequency,
            "avg_total_spectators": avg_total_spectators,
            "avg_first_week": avg_first_week,
            "avg_copies": avg_copies,
        }
    )

    # Normalisation des scores
    max_values = year_scores.max()
    normalized_scores = year_scores / max_values

    # Combinaison des scores normalisés
    normalized_scores["year_combined_score"] = normalized_scores.mean(axis=1)
    df = df.join(normalized_scores["year_combined_score"], on="year")
    save_files(df[["year", "year_combined_score"]], "year_scores")

    return df


def calculate_country_scores(df):
    # 1. Fréquence de distribution
    frequency = df["country"].value_counts()
    # 2. Moyenne des spectateurs totaux
    avg_total_spectators = df.groupby("country")["total_spectator"].mean()
    # 3. Moyenne de la première semaine
    avg_first_week = df.groupby("country")["first_week"].mean()
    # 4. Moyenne du nombre de copies
    avg_copies = df.groupby("country")["copies"].mean()

    # Compilation des scores dans un DataFrame
    distributor_scores = pd.DataFrame(
        {
            "frequency": frequency,
            "avg_total_spectators": avg_total_spectators,
            "avg_first_week": avg_first_week,
            "avg_copies": avg_copies,
        }
    )

    # Normalisation des scores
    max_values = distributor_scores.max()
    normalized_scores = distributor_scores / max_values

    # Combinaison des scores normalisés
    normalized_scores["country_combined_score"] = normalized_scores.mean(axis=1)
    df = df.join(normalized_scores["country_combined_score"], on="country")
    save_files(df[["country", "country_combined_score"]], "country_scores")

    return df


def drop_temp(df):
    df = df.drop(
        [
            # "actor_list",
            "date",
            "month",
            "day",
            "casting",
            "director",
            "raw_title",
            "distributor",
            "award",
            "lang",
            "first_day",
            "first_weekend",
            "hebdo_rank",
            "total_spectator",
            "rating_press",
            "budget",
            "genre",
        ],
        axis=1,
    )
    return df


def save_files(df, filename):
    # scores_json = df.to_dict('dict')
    # with open(f'modelisation/score_datasets/{filename}.json', 'w') as f:
    #     json.dump(scores_json, f, indent=4)
    model_path = f"modelisation/score_datasets/{filename}.pkl"
    dump(df, model_path)


def load_file(filename):
    return load(f"modelisation/score_datasets/{filename}.pkl")
