# DSA210-Personal-Movie-Database-Project

# MOTIVATION 

I am someone who watches movies regularly and enjoys discovering new directors, genres, and cinematic styles. Since I actively use Letterboxd to log my viewing history and favorite movies, I want to analyze my own movie-watching behavior using real data.

This project turns my viewing habits into a structured movie database and explores which factors shape the kinds of movies I enjoy the most.

# DATASET

1. Letterboxd Export

Includes: watched movies, ratings and favorites.

Used as the foundation, each movie in the Letterboxd list will be matched with metadata from external APIs.

2. TMDB API

Used to collect:

Movie titles

Release date, runtime

Genres

Cast and directors

3. OMDb API

Used to collect:

IMDb rating and votes

Rotten Tomatoes scores

Oscar wins/nominations

4. Additional Award Data (optional)

For more detailed award information, I may enrich the dataset using external sources containing major award nominations and wins.

# 🎬 Metadata Features I Will Analyze

The final dataset will include variables such as:

Genre(s)

Director

Main cast

Year of release

Runtime

IMDb rating

Rotten Tomatoes critic scores

Award wins and nominations

My personal rating/favoring (from Letterboxd)

Date watched

# ❓ Research Questions

I aim to answer questions such as:

1. What genre combinations attract me the most?

Do I prefer single-genre films or multi-genre hybrids?

2. Which actors or directors appear most often in movies I enjoy?

Do I have hidden favorites that I repeatedly gravitate toward?

3. How much do critical scores and award winnings affect my preferences?

Are the movies I love also critically acclaimed, or do I prefer niche/underrated films?

4. How do my watching habits change over time?

Trends across months and years (e.g., seasonality, mood-dependent watching habits)

# 🧪 Hypotheses

Null Hypothesis (H1₀):

My liked movies are evenly distributed across genres; there is no significant relationship between genre and whether I like a movie.

Alternative Hypothesis (H1):

My liked movies tend to concentrate in specific genres or genre combinations rather than being evenly distributed across all genres.

Null Hypothesis (H2₀):

The movies I choose to watch do not show any bias toward specific actors or directors.

Alternative Hypothesis (2):

I am more likely to choose movies that feature actors or directors I already know or like.

Null Hypothesis (H3₀):

There is no relationship between critical scores and my decision to watch a movie.

Alternative Hypothesis (H3):

I am more likely to watch movies with higher IMDb or Rotten Tomatoes scores.











