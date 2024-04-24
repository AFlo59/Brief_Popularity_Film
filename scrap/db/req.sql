-- pour utiliser les requête left join dans les notebooks
use films_db;
SET sql_mode=(SELECT REPLACE(@@sql_mode,'ONLY_FULL_GROUP_BY',''));

-- left join sur les films imdb et jp 
use films_db;
SELECT im.id_jp, jp.title as jp_title, jp.original_title as jp_original_title, im.title as im_title FROM films_jp jp
left join films_imdb im on jp.id = im.id_jp

-- set scraped
use films_db;
update films_jp jp
join films_imdb im on im.id_jp = jp.id
set scraped = 1

-- unset scraped
use films_db;
update films_jp jp
set scraped = 0

-- requete pour ML
SELECT jp.id, jp.url_jp, im.url as url_im, jp.raw_title, 
		YEAR(jp.date) AS year, 
		MONTH(jp.date) AS month, 
		DAY(jp.date) AS day, 
        im.director, im.casting, im.distributor, im.genre, im.genre_raw, jp.country, jp.duration, jp.first_day, jp.first_week, jp.first_weekend, jp.hebdo_rank, 
jp.total_spectator, jp.copies, im.rating_press, im.budget, im.lang, im.award 
FROM films_jp as jp
LEFT JOIN films_imdb im ON im.id_jp = jp.id 
where im.id_jp is not null and im.date = jp.date
order by jp.first_week desc

-- get list of unique actors
use films_db;
SELECT distinct(actor)
 FROM films_imdb as im
 join
   JSON_TABLE(
     im.casting,
     "$[*]"
     COLUMNS(
       actor VARCHAR(255) PATH "$"
     )
   ) as aa
   order by actor

-- nb spectateur par acteur
use films_db;
SELECT actor, sum(jp.first_week) as week, sum(jp.total_spectator) as total, count(im.id) as nb_film
FROM films_imdb as im
join
   JSON_TABLE(
     im.casting,
     "$[*]"
     COLUMNS(
       actor VARCHAR(255) PATH "$"
     )
   ) as aa
LEFT JOIN films_jp jp ON jp.id = im.id_jp 
where im.id_jp is not null and im.date = jp.date

group by actor
order by total desc

-- nb spectateur par distributeur
use films_db;
SELECT dist, sum(jp.first_week) as week, sum(jp.total_spectator) as total, count(im.id) as nb_film
FROM films_imdb as im
join
   JSON_TABLE(
     im.distributor,
     "$[*]"
     COLUMNS(
       dist VARCHAR(255) PATH "$"
     )
   ) as aa
LEFT JOIN films_jp jp ON jp.id = im.id_jp 
where im.id_jp is not null and im.date = jp.date

group by dist
order by total desc

-- nb spectateur par realisateur
use films_db;
SELECT REPLACE(im.director, '"', '') as director, sum(jp.first_week) as week, sum(jp.total_spectator) as total, count(im.id) as nb_film
FROM films_imdb as im
LEFT JOIN films_jp jp ON jp.id = im.id_jp 
where im.id_jp is not null and im.date = jp.date

group by im.director
order by total desc