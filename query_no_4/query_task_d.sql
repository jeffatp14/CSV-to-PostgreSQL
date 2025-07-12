SELECT 
    fm.movie_name, 
	fm.year, 
	fm.rating
	-- fm.gross, 
	-- dg.genre
FROM 
    movies_dw.fact_movies fm
JOIN 
    movies_dw.junction_movies_genre jmg ON fm.movie_id = jmg.movie_id
JOIN 
    movies_dw.dim_genre dg ON jmg.genre_id = dg.genre_id
WHERE
	dg.genre='Comedy' AND fm.gross is NOT NULL 
ORDER BY
	fm.gross DESC
LIMIT 5;
