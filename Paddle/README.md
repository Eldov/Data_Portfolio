# Paddle Take Home Challenge:
  
Candidate: Emili Fishwick.  
This challenge was requested for candidates for the position of Data Engineer at Paddle company.
  
Some of the tools used for completion:  
- VSCode,
- PoorSQL.com,
- Jupyter Notebooks,
- Snowflake Worksheets,
- Snowflake Documentation
- Python 3.10 venv,
- Spotify API Documentation,
- and lots and lots of research.  
   
## The Repository  

This repo consists of 2 main directories:
- **python_answers ->** contains a folder where the csv's are saved and the 2 main files are:  
  - ***spotify_take_home_challenge.py ->*** script from where the datasets are created, part 1 of the python section;
  - ***python_improvements.md ->*** part 2 of the python section.
  
- **sql_answers ->** contains the 2 main files:
  - ***sqL_question_1.sql ->*** answers the part 1 of the SQL section. Sums up  all the other 3 (non extra) files;
  - ***sqL_question_2.sql ->*** answers the part 2 of the SQL section.
 
 ## <a name="contents"></a> Contents  

This README can be organised the following way:  
 - **[Python Part 1: Spotify Datasets ->](#python-part-1-spotify-datasets)** guides you through the organization of the script and data frames in it, the origins of each column in the datasets, and some comments that I deemed necessary. The script it refers to can be found here: [spotify_take_home_challenge.py](https://github.com/Eldov/Paddle_EV/blob/main/python_answers/spotify_take_home_challenge.py);
 - **[Python Part 2: How you would you make your script more robust? ->](#python-part-2-how-you-would-you-make-your-script-more-robust)** answers the "How you would you make your script more robust?" question, part 2 of the python section. Can also be found here: [python_improvements.md](https://github.com/Eldov/Paddle_EV/blob/main/python_answers/python_improvements.md). 
 - **[SQL Part 1: Active Sellers ->](#sql-part-1-active-sellers)** answers the first part of the SQL section, describing some of the files present in the sql_answers folder better.  
 - **[SQL Part 2: GMV per Category ->](#sql-part-2-gmv-per-category)** answers the second part of the SQL section. Explains how the result should be read and its components. Gives options on how to get more detailed results.
 - **[Conclusion ->](#conclusion)** Concludes the challenge and general comments.
  
## <a name="python-part-1-spotify-datasets"></a> Python Part 1: Spotify Datasets  
*Return to [Contents](#contents)*  
  
The following table has two columns, one for each main function. In each function, a dataframe is generated and these are the names of each column in the main dataframes:  

|category_playlists| playlist |
| ----------- | ----------- |
| id PK| playlist_id FK id|
|description|album_type|
|name|id|
|tracks_url|name|
|total_tracks|popularity|
|snapshot_id|uri|
||playlist_added_at|
||followers|

The next tables show each required dataset and where their columns come from:
### category_playlists_records
*Description: contains the playlists found under category_id **latin***
|column name| origin | description |
| ----------- | ----------- | -------- |
| description | category_playlists.description| *the description of a playlist* |
| name | category_playlists.name| *the name of a playlist* |
| id | category_playlists.id| *unique ID of a playlist* |
|tracks_url|category_playlists.tracks_url| *the API url of the tracks that fall under a playlist* |
|total_tracks|category_playlists.total_tracks| *total number of tracks in a playlist* |

### playlist_records
*Description: contains the unique playlist IDs and the playlist followers*
|column name| origin | description |
| ----------- | ----------- | -------- |
| id | playlist.playlist_id| *unique ID of a playlist* |
|followers|playlist.followers| *the total number of follower's for the playlist* |

### tracks_records
*Description: unique tracks of playlists that fall into the ***latin*** category_id*
|column name| origin | description |
| ----------- | ----------- | -------- |
|album_type|playlist.album_type| *the type of album from which the track comes from* |
|id|playlist.id| *unique identifier of the track* |
|name|playlist.name| *a track's name* |
|popularity|playlist.popularity| *a track's popularity value at the time of the API call* |
|uri|playlist.uri| *a track's URI* |

### playlist_track_id_records
*Description: contains playlist_id-track_id combinations and the time at which a track was added to the playlist*
|column name| origin | description |
| ----------- | ----------- | -------- |
|playlist_id|playlist.playlist_id| *the ID of a playlist* |
|playlist_added_at|playlist.playlist_added_at| *time at which a track was added to the playlist* |
|track_id|playlist.id| *the ID of a track* |

### track_artist_id_records
*Description: contains track_id-artist_id combinations*
|column name| origin | description |
| ----------- | ----------- | -------- |
|track_id|playlist.id| *the ID of a track* |
|artist_id|playlist.artist_id| *the ID of an artist* |

### artists_records
*Description: unique artists found across tracks of playlists that fall into the ***latin*** category_id*
|column name| origin | description |
| ----------- | ----------- | -------- |
|id|playlist.artist_id| *unique artist identifier* |
|name|playlist.artist_name| *name of an artist* |


When looking at the code, you will notice that I had to drop some rows. In most cases, it was done to be safe as the first main dataframe, category_playlists, had some repeated playlists with same ids, names and number of tracks. Honestly, I do not understand why that was happening.  
  
The code was also made in a way that you can import its functions, but it can be run normally and will create the csv.gz files as usual.  
I also did my best to explain what each for loop does. To be honest, I am not happy with the number of loops and do not think this is efficient, but I could not think of another way of doing it. I sincerely apologise for this.  
  
> :warning: **Attention:** Before running, make sure the csv subdirectory exists in the same folder you saved the *.py* file. Also make sure your terminal is in the directory that contains this very *.py* file.  

## <a name="python-part-2-how-you-would-you-make-your-script-more-robust"></a> Python Part 2: How you would you make your script more robust?  
*Return to [Contents](#contents)*  
  
- **Spotipy ->** I would use the Spotipy library. Forgive me if I misunderstood the assignment but, my understing was that I was not supposed to use it. In any case, many of my for loops would be smaller/inexistent by using the lib. The pagination would also be simpler.
  
- **Airflow ->** Because the category_type is defined inside the .env file, changing categories wouldn't be a problem. For a frequent use, I would use an orchestrator such as Airflow and save these datasets in a database, like PostGresQL. Adding SQLAlchemy to the code, deciding how the batches of data will be added to the database, update, append, replace, etc, depending on what changes should be tracked. 
  
- **Category Playslists Pagination ->** It lacks a pagination process on the first main dataframe creation. It did not seem necessary under ***latin*** category as it had less than 50 results but the limit was 50. For categories with more than 50 results, this code will encounter an error. Adding pagination to that specific part would avoid that, though, not necessary in this very case.
  
This answer is also present in the python_improvements.md file, found in this very repo (Python folder).
  
The .env file is just an example, please, change the variables before running this code or you will have errors.  
The compressed csv files will be saved in a folder called csv.
  
## <a name="sql-part-1-active-sellers"></a> SQL Part 1: Active Sellers  
*Return to [Contents](#contents)*  
  
Here the final result can be found by running the query in the file [sql_question_1.sql](https://github.com/Eldov/Paddle_EV/blob/main/sql_answers/sql_question_1.sql).  
You will also notice there are 4 other files in this directory. This happens because I answered each question separately and you can check each of them with more detail in their files.  
You will also notice there is an extra file called [1-SQL-extra-sellers-sold-daily-on-avg.txt](https://github.com/Eldov/Paddle_EV/blob/main/sql_answers/1-SQL-extra-sellers-sold-daily-on-avg.txt). This file exists because I was not sure about how to calculate the daily part of this assignement.  
Could it be the average of sellers that sold every day, or sellers that sold every day on average? This extra file tries to answer the latter.  
  
## <a name="sql-part-2-gmv-per-category"></a> SQL Part 2: GMV per Category  
*Return to [Contents](#contents)*  
  
Here the final result can be found by running the query in the file [sql_question_2.sql](https://github.com/Eldov/Paddle_EV/blob/main/sql_answers/sql_question_2.sql).
This query results in a table that has 4 columns:  

- **WEEK:** the week of the 2017 year;
- **PRODUCT_CATEGORY:** the category this row refers to. Can be 1 of the 3 that sold the most in November the same year;
- **GMV:** gross merchandise value, sum of the price of each order of that category on that specific week;
- **GMV_GROWTH_RATE:** the variation from the pior week in comparison with the current week. Really important to pay attention, this compares weeks for the same category. The line before is not necessarly the 1 you should be checking, but the same category's week before.

If you want to run the code checking the lag, in other words, the GMV of that category in the previous week, you can uncomment line 48.  
```  
//w2.weekly_gmv AS weekly_gmv_lag  
```  
If you want to check a specific category, uncomment line 59 making sure it has the category you want to specify.  
```  
//HAVING product_category = 'cama_mesa_banho'  
```  

## <a name="conclusion"></a> Conclusion  
*Return to [Contents](#contents)*  
  
This challenge was really enriching for me as I could learn a lot about the Spotify API and Snowflake. One of my first ideas was to use the Snowflake Connector so I also learned a lot about it and would be happy to discuss it and share my findings.  

To conclude, I do not think this is the most efficient nor clean solution that I could have achieved but it would require more experience and opinions from my peers, which I would love to have. I would appreciate your feedback on what I can improve and new ideas on how I could have solved this, maybe something less complex.  

I thank you deeply for the opportunity, your patience and for taking time to check my code. Please feel free to contact me as feedback will be much appreciated.  
