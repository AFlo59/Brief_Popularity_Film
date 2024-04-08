use films_db;
SET sql_mode=(SELECT REPLACE(@@sql_mode,'ONLY_FULL_GROUP_BY',''));

SELECT fa1.id_jp, jp.`year`, fa1.year_allo, jp.director, jp.title, fa1.director_allo, jp.url_jp, fa1.url_allo
-- , jp.title, jp.`year`, jp.director, fa1.year_allo, fa1.director_allo 

-- jp.country, jp.duration, jp.genre, jp.first_day, jp.first_week, jp.first_weekend, jp.hebdo_rank, jp.total_spectator, jp.copies,
-- fa1.rating_press, fa1.rating_public, fa1.casting, fa1.budget, fa1.lang, fa1.visa, fa1.award

FROM films_jp as jp
LEFT JOIN films_allo fa1 ON fa1.id_jp = jp.id
                        
where fa1.year_allo is not null and fa1.year_allo != -1
group by fa1.id_jp, jp.`year`, jp.director