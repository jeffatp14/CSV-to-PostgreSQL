-- Create schema (if not exists)
CREATE SCHEMA IF NOT EXISTS movies_dw;

-- -- Drop tables 
DROP TABLE IF EXISTS 
    movies_dw.junction_movie_stars,
    movies_dw.junction_movie_directors,
    movies_dw.junction_movies_genre,
    movies_dw.dim_stars,
    movies_dw.dim_directors,
    movies_dw.dim_genre,
    movies_dw.fact_movies,
	movies_dw.raw_movies
CASCADE;

-- 1. Fact Table: Movies
CREATE TABLE movies_dw.fact_movies (
    movie_id SERIAL PRIMARY KEY,
    movie_name TEXT NOT NULL,
	year TEXT,
	rating NUMERIC(3, 2),  
    one_line TEXT,
    runtime SMALLINT,
    gross NUMERIC(15, 2)
);

-- 2. Dimension Table: Genres
CREATE TABLE movies_dw.dim_genre (
    genre_id SERIAL PRIMARY KEY,
    genre VARCHAR(50) NOT NULL
);

-- 3. Dimension Table: Directors
CREATE TABLE movies_dw.dim_directors (
    director_id SERIAL PRIMARY KEY,
    director VARCHAR(100)
);

-- 4. Dimension Table: Stars
CREATE TABLE movies_dw.dim_stars (
    star_id SERIAL PRIMARY KEY,
    stars VARCHAR(100) NOT NULL
);

-- 5. Junction Table: Movies & Genres
CREATE TABLE movies_dw.junction_movies_genre (
    movie_id INT NOT NULL,
    genre_id INT NOT NULL,
    PRIMARY KEY (movie_id, genre_id),
    FOREIGN KEY (movie_id) REFERENCES movies_dw.fact_movies(movie_id),
    FOREIGN KEY (genre_id) REFERENCES movies_dw.dim_genre(genre_id)
);

-- 6. Junction Table: Movies & Directors
CREATE TABLE movies_dw.junction_movie_directors (
    movie_id INT NOT NULL,
    director_id INT NOT NULL,
    PRIMARY KEY (movie_id, director_id),
    FOREIGN KEY (movie_id) REFERENCES movies_dw.fact_movies(movie_id),
    FOREIGN KEY (director_id) REFERENCES movies_dw.dim_directors(director_id)
);

-- 7. Junction Table: Movies & Stars
CREATE TABLE movies_dw.junction_movie_stars (
    movie_id INT NOT NULL,
    star_id INT NOT NULL,
    PRIMARY KEY (movie_id, star_id),
    FOREIGN KEY (movie_id) REFERENCES movies_dw.fact_movies(movie_id),
    FOREIGN KEY (star_id) REFERENCES movies_dw.dim_stars(star_id)
);
-- 8. Raw table
CREATE TABLE movies_dw.raw_movies (
movie_id SERIAL PRIMARY KEY,
    movie_name TEXT,
    year TEXT,
    genre TEXT,
    director TEXT,
    stars TEXT,
    rating NUMERIC,
    one_line TEXT,
    runtime NUMERIC,
    gross TEXT
);