SELECT  name, releasedate FROM album
WHERE releasedate BETWEEN '2018-01-01' AND '2018-12-31';


SELECT   name, tracklength FROM track
ORDER BY tracklength DESC;


SELECT  name FROM track
WHERE tracklength >= 03.50;


SELECT name FROM collections
WHERE release_year BETWEEN '2018-01-01' AND '2020-12-31';


SELECT name FROM artist
WHERE name NOT LIKE '%% %%';


SELECT name FROM track
WHERE name LIKE '%%my%%';
