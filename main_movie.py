import requests
import pandas as pd
from datetime import datetime
import os

# Load TMDB API key
API_KEY = os.getenv('TMDB_API_KEY') or input("Enter your TMDb API key: ")

class MovieDataCollector:
    def __init__(self, filename="movie_dataset.csv"):
        self.filename = filename

        # If CSV exists → load it
        if os.path.exists(filename):
            print(f"📂 Existing dataset found. Loading {filename}...")
            self.movies_df = pd.read_csv(filename)

            # Convert list-like strings back to lists
            list_columns = ['genres', 'directors', 'cast', 'countries']
            for col in list_columns:
                if col in self.movies_df.columns:
                    self.movies_df[col] = self.movies_df[col].apply(
                        lambda x: eval(x) if isinstance(x, str) else x
                    )

            print(f"Loaded {len(self.movies_df)} movies.")

        else:
            print("🆕 No dataset found. Starting a new one.")
            self.movies_df = pd.DataFrame(columns=[
                'movie_id', 'title', 'release_year', 'release_date',
                'runtime', 'genres', 'directors', 'cast',
                'countries', 'collection_date'
            ])

    def extract_movie_data(self, movie_data):
        """Extract and structure movie data from TMDB API response"""

        movie_id = movie_data.get('id')
        title = movie_data.get('title', 'Unknown')

        release_date = movie_data.get('release_date', '')
        release_year = release_date[:4] if release_date else 'Unknown'
        runtime = movie_data.get('runtime')

        # Genres
        genres = [g['name'] for g in movie_data.get('genres', [])]

        # Directors
        directors = []
        for p in movie_data.get('credits', {}).get('crew', []):
            if p.get('job') == 'Director':
                directors.append(p.get('name'))

        # Cast (top 15)
        cast = [actor['name'] for actor in movie_data.get('credits', {}).get('cast', [])[:15]]

        # Countries
        countries = [c['name'] for c in movie_data.get('production_countries', [])]

        # Timestamp
        collection_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        return {
            'movie_id': movie_id,
            'title': title,
            'release_date': release_date,
            'release_year': release_year,
            'runtime': runtime,
            'genres': genres,
            'directors': directors,
            'cast': cast,
            'countries': countries,
            'collection_date': collection_date
        }

    def add_movie_to_dataframe(self, movie_data):
        """Add structured movie data to the DataFrame"""

        structured_data = self.extract_movie_data(movie_data)

        # Avoid duplicates
        if structured_data['movie_id'] in self.movies_df['movie_id'].values:
            print(f"⚠️ '{structured_data['title']}' is already in the dataset. Skipping.")
            return

        # Append
        new_row = pd.DataFrame([structured_data])
        self.movies_df = pd.concat([self.movies_df, new_row], ignore_index=True)

        print(f"✅ Added '{structured_data['title']}' (Total: {len(self.movies_df)} movies)")

    def save_to_csv(self, filename=None):
        """Save DataFrame to CSV"""

        if filename is None:
            filename = self.filename

        if not self.movies_df.empty:
            self.movies_df.to_csv(filename, index=False)
            print(f"💾 Data saved to {filename}")
        else:
            print("❌ No data to save")

    def display_dataset_info(self):
        if self.movies_df.empty:
            print("📊 Dataset is empty.")
            return

        print(f"\n📊 Dataset Information:")
        print(f"   Total movies: {len(self.movies_df)}")
        print(f"   Columns: {list(self.movies_df.columns)}")
        print(f"   Latest addition: {self.movies_df.iloc[-1]['title']}")

    def get_movie_statistics(self):
        if self.movies_df.empty:
            print("No data available.")
            return

        print(f"\n📈 Dataset Statistics:")
        print(f"   Total movies: {len(self.movies_df)}")
        print(f"   Average runtime: {self.movies_df['runtime'].mean():.1f} minutes")

        # Genre frequencies
        all_genres = [genre for sub in self.movies_df['genres'] for genre in sub]
        genre_counts = pd.Series(all_genres).value_counts()
        if not genre_counts.empty:
            print(f"   Most common genre: {genre_counts.index[0]}")

        # Director frequencies
        all_directors = [d for sub in self.movies_df['directors'] for d in sub]
        director_counts = pd.Series(all_directors).value_counts()
        if not director_counts.empty:
            print(f"   Most frequent director: {director_counts.index[0]} ({director_counts.iloc[0]} movies)")


######################################################################################################

def display_movie_info(movie_data):
    credits = movie_data.get('credits', {})
    cast_data = credits.get('cast', [])[:10]

    directors = [p['name'] for p in credits.get('crew', []) if p.get('job') == 'Director']
    genres = [g['name'] for g in movie_data.get('genres', [])]

    release_date = movie_data.get('release_date', 'Unknown')
    runtime = movie_data.get('runtime', 'Unknown')

    print(f"\n🎬 {movie_data['title']} ({release_date[:4] if release_date != 'Unknown' else 'Unknown'})")
    print(f"⏱️ Runtime: {runtime} minutes")
    print(f"🎭 Genres: {', '.join(genres)}")
    print(f"🎥 Directors: {', '.join(directors)}")

    print("\n🌟 Main Cast:")
    for i, actor in enumerate(cast_data, 1):
        print(f"   {i}. {actor['name']} as {actor.get('character')}")


#######################################################################################################

def interactive_movie_search():
    collector = MovieDataCollector()

    while True:
        print("\n" + "🎬" * 20)
        print("1. Search for a movie")
        print("2. Show dataset info")
        print("3. Show statistics")
        print("4. Save dataset")
        print("5. Exit")

        choice = input("Select option (1-5): ").strip()

        if choice == '1':
            movie_title = input("Enter movie title: ").strip()
            if not movie_title:
                continue

            # Search
            search_url = "https://api.themoviedb.org/3/search/movie"
            params = {'api_key': API_KEY, 'query': movie_title}

            response = requests.get(search_url, params=params)
            data = response.json()

            if not data['results']:
                print(f"❌ No results for '{movie_title}'")
                continue

            # Handle multiple results
            results = data['results'][:5]
            if len(results) > 1:
                print("\nTop results:")
                for i, movie in enumerate(results, 1):
                    year = movie.get('release_date', '')[:4]
                    print(f"{i}. {movie['title']} ({year})")

                selection = input("Choose number (Enter=first): ").strip()
                if selection.isdigit() and 1 <= int(selection) <= len(results):
                    selected_movie = results[int(selection) - 1]
                else:
                    selected_movie = results[0]
            else:
                selected_movie = results[0]

            movie_id = selected_movie['id']

            # Get detailed info
            movie_url = f"https://api.themoviedb.org/3/movie/{movie_id}"
            movie_params = {
                'api_key': API_KEY,
                'append_to_response': 'credits'
            }

            movie_response = requests.get(movie_url, params=movie_params)
            movie_data = movie_response.json()

            collector.add_movie_to_dataframe(movie_data)
            display_movie_info(movie_data)

        elif choice == '2':
            collector.display_dataset_info()

        elif choice == '3':
            collector.get_movie_statistics()

        elif choice == '4':
            collector.save_to_csv()

        elif choice == '5':
            if not collector.movies_df.empty:
                save = input("Save before exit? (y/n): ").strip().lower()
                if save == 'y':
                    collector.save_to_csv()

            print("Goodbye! 👋")
            break

        else:
            print("❌ Invalid option.")


if __name__ == "__main__":
    interactive_movie_search()
