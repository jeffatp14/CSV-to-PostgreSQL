SELECT 
    fm.movie_name, 
	fm.year, 
	fm.rating
	-- ds.stars, 
	-- dd.director
FROM 
    movies_dw.fact_movies fm
JOIN 
    movies_dw.junction_movie_stars jms ON fm.movie_id = jms.movie_id
JOIN 
    movies_dw.dim_stars ds ON jms.star_id = ds.star_id
JOIN 
    movies_dw.junction_movie_directors jmd ON fm.movie_id = jmd.movie_id
JOIN 
    movies_dw.dim_directors dd ON jmd.director_id = dd.director_id
WHERE
	dd.director='Martin Scorsese' AND ds.stars='Robert De Niro';
