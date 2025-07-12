SELECT 
    fm.movie_name, 
    fm.year, 
    fm.rating
	-- ds.stars
FROM 
    movies_dw.fact_movies fm
JOIN 
    movies_dw.junction_movie_stars jms ON fm.movie_id = jms.movie_id
JOIN 
    movies_dw.dim_stars ds ON jms.star_id = ds.star_id
WHERE 
    ds.stars = 'Lena Headey'
ORDER BY 
    fm.year;

