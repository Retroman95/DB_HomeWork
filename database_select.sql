SELECT year, name FROM album
       WHERE year = 2018;

SELECT length, name FROM track
       ORDER BY length DESC
	   LIMIT 1;

SELECT length, name FROM track
       WHERE length >= 210;

SELECT year, name FROM collection
       WHERE year BETWEEN 2018 AND 2020;

SELECT name FROM artist
       WHERE name NOT LIKE '%% %%';

SELECT name FROM track
       WHERE name LIKE '%%My%%';
