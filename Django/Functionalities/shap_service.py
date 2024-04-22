import matplotlib.pyplot as plt
from .models import FilmScrap


def get_graph():
    req = """SELECT 
                  id,
                  YEAR(date) AS year, 
                  MONTH(date) AS month, 
                  DAY(date) AS day, 
                  director, distributor, casting, duration, country, genre
                FROM functionalities_filmscrap
                LIMIT 2
              """
    films = FilmScrap.objects.raw(req)
    return films
