theaters ( _th_name_, capacity)

movies (_imdb_key_, title, year, running_time)

customers (_user_name_, full_name, password)

screenings (/th_name/, /imdb_key/, start_time, start_date)

ticets (_t_id_, /th_name/, /imdb_key/,start_time, start_date)

7)

SELECT th_name, imdb_key, start_time, start_date, capacity - count()
FROM theaters
JOIN ticets
USING th_name
GROUP BY th_name, imdb_key, start_time, start_date

SELECT th_name, imdb_key, start_time, start_date, count()
FROM screenings
JOIN ticets
USING (th_name, imdb_key, start_time, start_date)
GROUP BY th_name, imdb_key, start_time, start_date

8)
