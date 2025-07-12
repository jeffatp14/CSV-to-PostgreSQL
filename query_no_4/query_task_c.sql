SELECT 
	dd.director, 
	sum(fm.gross) as total_gross_million
FROM 
    movies_dw.fact_movies fm
JOIN 
    movies_dw.junction_movie_directors jmd ON fm.movie_id = jmd.movie_id
JOIN 
    movies_dw.dim_directors dd ON jmd.director_id = dd.director_id
GROUP BY 
	dd.director
ORDER BY
	total_gross_million ASC
