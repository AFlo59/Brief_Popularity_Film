exit
scrapy crawl all_movies
scrapy crawl allocine_movies
alembic revision --autogenerate -m "
alembic upgrade head
