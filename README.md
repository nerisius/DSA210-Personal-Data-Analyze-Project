# DSA210-Personal-Movie-Database-Project

# MOTIVATION 

I have been logging my cinema journey since age 15. This project aims to move beyond simple recording to understand the underlying patterns of my taste. 

# 📦DATASET

## 1. Letterboxd Export

Includes: watched movies, ratings and favorites.

Used as the foundation, each movie in the Letterboxd list will be matched with metadata from external APIs.

## 2. TMDB API

Movie titles

Release date, runtime

Genres

Cast and directors

## 3. OMDb API

IMDb rating and votes

Rotten Tomatoes scores

Oscar wins/nominations


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

# ❓ Research Questions

I aim to answer questions such as:

1. What genre combinations attract me the most?

Do I prefer single-genre films or multi-genre hybrids?

2. Which actors or directors appear most often in movies I enjoy?

Do I have hidden favorites that I repeatedly gravitate toward?

3. How much do critical scores and award winnings affect my preferences?

Are the movies I love also critically acclaimed, or do I prefer niche/underrated films?


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


# 📊 Key Findings & Results

Genre Analysis: I found a strong preference for Comedy and Comedy-Drama combination.

Actor and Director Bias: While there's no significant evidence that shows a bias towards directors, some actors appear significantly more than others in the movies ı watched.

Critical Scores: Movies ı watch have significantly higher critical scores than certain benchmarks, which are 7.5 imdb and 75% RT

# 🤖 Machine Learning Implementation

I implemented a Logistic Regression to predict whether I would "Like" a movie (binary classification) based on:

Features: genre, IMDb Score, RT score, runtime, oscar_wins, oscar_nominations.

The Outcome: The model performed poorly, achieving an overall accuracy of only 25% and an F1-score of 0.27. To improve accuracy, ı added other variables such as actors and directors but instead of improving, it dropped significantly.

The Recall Paradox: The model achieved a high Recall (0.94) for "Liked" movies, meaning it caught almost all of my favorites. However, its Precision (0.16) was very low, it predicted a "Like" for almost every movie I watched.

The Interpretation: The metadata (Genre, Runtime, IMDb Score) is not enough to define my taste. My preference is governed by subjective variables that aren't captured in a standard database such as cinematography style, emotional resonance, or the specific mood I was in when watching.












