exit
scrapy crawl all_movies
scrapy crawl imdb_movies
scrapy crawl imdb_top10_movies
scrapy crawl allocine_seances
alembic revision --autogenerate -m "
alembic upgrade head
exit
