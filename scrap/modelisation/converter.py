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

    val = []
    for index, row in df.iterrows():
        try:
            found = scores.loc[scores[column] == df.iloc[index][column]]
            val.append(found.iloc[0]["director_combined_score"])
        except Exception:
            val.append(0.1)

    df["director_combined_score"] = pd.Series(val)
    return df


def convert_actor(df, column):
    scores = load_file("actor_scores")

    df["actor_combined_score"] = 0

    val = []
    for index, row in df.iterrows():
        sum = 0
        try:
            df_actors = df.iloc[index][column]
            for actor in df_actors:
                found = scores.loc[scores["actor"] == actor]
                if found.shape[0] != 0:
                    sum += found.iloc[0]["actor_combined_score"]
        except Exception:
            pass

        val.append(sum)

    df["actor_combined_score"] = pd.Series(val)
    return df


def convert_distributor(df, column):
    scores = load_file("distributor_scores")

    df["distributor_combined_score"] = 0

    val = []
    for index, row in df.iterrows():
        sum = 0
        try:
            df_distributors = df.iloc[index][column]
            for distributor in df_distributors:
                found = scores.loc[scores["distributor"] == distributor]
                if found.shape[0] != 0:
                    sum += found.iloc[0]["distributor_combined_score"]
        except Exception:
            pass

        val.append(sum)

    df["distributor_combined_score"] = pd.Series(val)
    return df