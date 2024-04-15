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
        im.director, im.casting, im.distributor, jp.country, jp.duration, jp.genre, jp.first_day, jp.first_week, jp.first_weekend, jp.hebdo_rank, 
jp.total_spectator, jp.copies, im.rating_press, im.budget, im.lang, im.award 
FROM films_jp as jp
LEFT JOIN films_imdb im ON im.id_jp = jp.id 
where im.id_jp is not null and im.date = jp.date
order by jp.first_week desc