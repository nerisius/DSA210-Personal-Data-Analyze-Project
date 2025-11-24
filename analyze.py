import pandas as pd
from itertools import combinations
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_csv("movie_dataset.csv")

# directors, cast, genres, countries columns may be stored as strings; convert them to lists
for col in ['directors', 'cast', 'genres', 'countries']:
    if col in df.columns:
        df[col] = df[col].apply(lambda x: eval(x) if isinstance(x, str) else x)


def plot_barh_with_values(series, title, color, x_min=0):
    fig, ax = plt.subplots(figsize=(12,8))
    bars = ax.barh(series.index, series.values, color=color)
    ax.bar_label(bars, fmt='%d', padding=3)  #write values on bars
    ax.set_xlim(left=x_min) 
    ax.set_xlabel("Movie Count")
    ax.set_ylabel(title)
    ax.set_title(title)
    ax.invert_yaxis()  # highest values on top
    plt.tight_layout()
    plt.show()

# directors
all_directors = [d for sublist in df['directors'] for d in sublist]
director_counts = pd.Series(all_directors).value_counts()
print(director_counts.head(10))
plot_barh_with_values(director_counts.head(10), "Most watched directors", "skyblue", x_min=5)

# cast
all_actors = [a for sublist in df['cast'] for a in sublist]
actor_counts = pd.Series(all_actors).value_counts()
print(actor_counts.head(15))
plot_barh_with_values(actor_counts.head(15), "Most watched actors", "orange", x_min=5)

#Most watched genres
all_genres = [g for sublist in df['genres'] for g in sublist]
genre_counts = pd.Series(all_genres).value_counts()
print("\n🎭 En çok izlediğin türler:")
print(genre_counts.head(15))
plot_barh_with_values(genre_counts.head(15), "Most watched genres", "green", x_min=5)


# IMDb Rating Distribution
if 'imdb_rating' in df.columns:
    df['imdb_rating'] = pd.to_numeric(df['imdb_rating'], errors='coerce')

    plt.figure(figsize=(10,6))
    sns.histplot(df['imdb_rating'].dropna(), bins=20, color='purple', alpha=0.7)
    plt.xlabel("IMDb Rating")
    plt.ylabel("Number of Movies")
    plt.title("IMDb Rating Distribution")
    plt.xlim(0, 10)  # IMDb ratings are 0-10
    plt.show()

# Rotten Tomatoes Distribution
if 'rt_rating' in df.columns:
    # Convert percentage string to float
    df['rt_rating'] = df['rt_rating'].str.replace('%','').astype(float)

    plt.figure(figsize=(10,6))
    sns.histplot(df['rt_rating'].dropna(), bins=20, color='red', alpha=0.7)
    plt.xlabel("Rotten Tomatoes (%)")
    plt.ylabel("Number of Movies")
    plt.title("Rotten Tomatoes Distribution")
    plt.xlim(0, 100)  # RT is 0-100%
    plt.show()


# oscars
if 'oscar_wins' in df.columns:
    df['oscar_wins'] = pd.to_numeric(df['oscar_wins'], errors='coerce').fillna(0)
    df['oscar_nominations'] = pd.to_numeric(df['oscar_nominations'], errors='coerce').fillna(0)

    won_any = df[df['oscar_wins'] > 0]
    print(f"\n🏆 Oscar kazanmış film sayısı: {len(won_any)} / {len(df)}")


# Assume your dataframe is df and 'genres' column is list of genres
# Make sure genres are lists, not strings
df['genres'] = df['genres'].apply(lambda x: eval(x) if isinstance(x, str) else x)

# Get unique genres
unique_genres = sorted({g for sublist in df['genres'] for g in sublist})

# Create co-occurrence matrix
co_matrix = pd.DataFrame(0, index=unique_genres, columns=unique_genres)

for genres in df['genres']:
    if isinstance(genres, list):
        for g1, g2 in combinations(genres, 2):
            co_matrix.at[g1, g2] += 1
            co_matrix.at[g2, g1] += 1  # symmetric

# Fill diagonal with counts of individual genres
for g in unique_genres:
    co_matrix.at[g, g] = sum(g in genres for genres in df['genres'])

# Plot heatmap
plt.figure(figsize=(12,10))
sns.heatmap(co_matrix, annot=True, fmt="d", cmap="YlGnBu")
plt.title("Genre Co-occurrence Heatmap")
plt.show()