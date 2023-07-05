## Python Part 1: How you would you make your script more robust?

- **Spotipy ->** I would use the Spotipy library. Forgive me if I misunderstood the assignment but, my understing was that I was not supposed to use it. In any case, many of my for loops would be smaller/inexistent by using the lib. The pagination would also be simpler.
  
- **Airflow ->** Because the category_type is defined inside the .env file, changing categories wouldn't be a problem. For a frequent use, I would use an orchestrator as Airflow and save these datasets in a database, like PostGresQL. Adding SQLAlchemy to the code, deciding how the batches of data will be added to the database, update, append, replace, etc, depending on what changes should be tracked. 

- **Playslist Pagination ->** It lacks a pagination process on the first main dataframe creation. It did not seem necessary under ***latin*** category as it had less than 50 results but the limit was 50. For categories with more than 50 results, this code will encounter an error. Adding pagination to that specific part would avoid that, though, not necessary in this very case.