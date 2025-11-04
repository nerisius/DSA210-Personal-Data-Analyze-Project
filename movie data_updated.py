import requests
import pandas as pd
from datetime import datetime
import os
import json

# Get API key from environment variable or user input
API_KEY = os.getenv('TMDB_API_KEY') or input("Enter your TMDb API key: ")

class MovieDataCollector:
    def __init__(self):
        # Initialize DataFrame with proper column structure
        self.movies_df = pd.DataFrame(columns=[
            'movie_id', 'title', 'release_year', 'runtime', 
            'genres', 'directors', 'cast'
        ])

    def extract_movie_data(self, movie_data):
        """Extract and structure movie data from API response"""
        
        # Basic movie info
        movie_id = movie_data.get('id')
        title = movie_data.get('title', 'Unknown')
        release_date = movie_data.get('release_date', '')
        release_year = release_date[:4] if release_date else 'Unknown'
        runtime = movie_data.get('runtime')

        # Extract genres as list
        genres = [genre['name'] for genre in movie_data.get('genres', [])]
        
        # Extract directors
        credits_data = movie_data.get('credits', {})
        directors = []
        for person in credits_data.get('crew', []):
            if person['job'] == 'Director':
                directors.append(person['name'])
        
        # Extract cast with character information (top 10)
        cast = []
        for actor in credits_data.get('cast', [])[:10]:
            cast.append(actor['name'])
        
        # Current timestamp for data collection
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
            'collection_date': collection_date
        }
    
    def add_movie_to_dataframe(self, movie_data):
        """Add movie data to the DataFrame"""
        structured_data = self.extract_movie_data(movie_data)
        
        # Convert to DataFrame row and append
        new_row = pd.DataFrame([structured_data])
        self.movies_df = pd.concat([self.movies_df, new_row], ignore_index=True)
        
        print(f"✅ Added '{structured_data['title']}' to dataset (Total: {len(self.movies_df)} movies)")
    
    def save_to_csv(self, base_filename="movie_dataset"):
        """Save DataFrame to multiple CSV files - one main file and separate files for each variable"""
        if self.movies_df.empty:
            print("❌ No data to save")
            return False
        
        # 1. Save main combined CSV
        main_file = f"{base_filename}.csv"
        self.movies_df.to_csv(main_file, index=False)
        print(f"💾 Main dataset saved to {main_file}")
        
        # 2. Save basic info CSV (movie_id, title, release_year, runtime)
        basic_info_df = self.movies_df[['movie_id', 'title', 'release_year', 'runtime']].copy()
        basic_file = f"{base_filename}_basic_info.csv"
        basic_info_df.to_csv(basic_file, index=False)
        print(f"💾 Basic info saved to {basic_file}")
        
        # 3. Save genres CSV (expanded - one row per movie-genre pair)
        genres_data = []
        for _, row in self.movies_df.iterrows():
            movie_id = row['movie_id']
            title = row['title']
            for genre in row['genres']:
                genres_data.append({
                    'movie_id': movie_id,
                    'title': title,
                    'genre': genre
                })
        if genres_data:
            genres_df = pd.DataFrame(genres_data)
            genres_file = f"{base_filename}_genres.csv"
            genres_df.to_csv(genres_file, index=False)
            print(f"💾 Genres saved to {genres_file}")
        
        # 4. Save directors CSV (expanded - one row per movie-director pair)
        directors_data = []
        for _, row in self.movies_df.iterrows():
            movie_id = row['movie_id']
            title = row['title']
            for director in row['directors']:
                directors_data.append({
                    'movie_id': movie_id,
                    'title': title,
                    'director': director
                })
        if directors_data:
            directors_df = pd.DataFrame(directors_data)
            directors_file = f"{base_filename}_directors.csv"
            directors_df.to_csv(directors_file, index=False)
            print(f"💾 Directors saved to {directors_file}")
        
        # 5. Save cast CSV (expanded - one row per movie-actor pair with position)
        cast_data = []
        for _, row in self.movies_df.iterrows():
            movie_id = row['movie_id']
            title = row['title']
            for position, actor in enumerate(row['cast'], 1):
                cast_data.append({
                    'movie_id': movie_id,
                    'title': title,
                    'actor': actor,
                    'cast_position': position
                })
        if cast_data:
            cast_df = pd.DataFrame(cast_data)
            cast_file = f"{base_filename}_cast.csv"
            cast_df.to_csv(cast_file, index=False)
            print(f"💾 Cast saved to {cast_file}")
        
        # 6. Save release years CSV (for temporal analysis)
        years_df = self.movies_df[['movie_id', 'title', 'release_year']].copy()
        years_file = f"{base_filename}_release_years.csv"
        years_df.to_csv(years_file, index=False)
        print(f"💾 Release years saved to {years_file}")
        
        # 7. Save runtime CSV (for runtime analysis)
        runtime_df = self.movies_df[['movie_id', 'title', 'runtime']].copy()
        runtime_file = f"{base_filename}_runtime.csv"
        runtime_df.to_csv(runtime_file, index=False)
        print(f"💾 Runtime data saved to {runtime_file}")
        
        print(f"\n✨ Successfully created 7 CSV files!")
        return True
    
    def display_dataset_info(self):
        """Display basic information about the dataset"""
        if not self.movies_df.empty:
            print(f"\n📊 Dataset Information:")
            print(f"   Total movies: {len(self.movies_df)}")
            print(f"   Columns: {list(self.movies_df.columns)}")
            print(f"   Latest addition: {self.movies_df.iloc[-1]['title']}")
        else:
            print("📊 Dataset is empty")
    
    def get_movie_statistics(self):
        """Display some basic statistics about the collected data"""
        if self.movies_df.empty:
            print("No data available for statistics")
            return
        
        print(f"\n📈 Dataset Statistics:")
        print(f"   Total movies: {len(self.movies_df)}")
        
        # Runtime statistics
        valid_runtimes = self.movies_df['runtime'].dropna()
        if not valid_runtimes.empty:
            print(f"   Average runtime: {valid_runtimes.mean():.2f} minutes")
        
        # Genre frequency
        all_genres = [genre for sublist in self.movies_df['genres'] for genre in sublist]
        if all_genres:
            genre_counts = pd.Series(all_genres).value_counts()
            print(f"   Most common genre: {genre_counts.index[0]} ({genre_counts.iloc[0]} movies)")
            print(f"   Total unique genres: {len(genre_counts)}")
        
        # Director frequency
        all_directors = [director for sublist in self.movies_df['directors'] for director in sublist]
        if all_directors:
            director_counts = pd.Series(all_directors).value_counts()
            print(f"   Most frequent director: {director_counts.index[0]} ({director_counts.iloc[0]} movies)")
            print(f"   Total unique directors: {len(director_counts)}")
        
        # Cast statistics
        all_cast = [actor for sublist in self.movies_df['cast'] for actor in sublist]
        if all_cast:
            cast_counts = pd.Series(all_cast).value_counts()
            print(f"   Most frequent actor: {cast_counts.index[0]} ({cast_counts.iloc[0]} movies)")
            print(f"   Total unique actors: {len(cast_counts)}")


##################################################################################################################################################
def interactive_movie_search():
    collector = MovieDataCollector()
    
    while True:
        print("\n" + "🎬" * 20)
        print("1. Search for a movie")
        print("2. Show dataset info")
        print("3. Show statistics")
        print("4. Save to CSV files")
        print("5. Exit")
        
        choice = input("\nSelect option (1-5): ").strip()
        
        if choice == '1':
            movie_title = input("Enter movie title: ").strip()
            
            if not movie_title:
                continue
            
            # Search for movie
            search_url = "https://api.themoviedb.org/3/search/movie"
            params = {'api_key': API_KEY, 'query': movie_title}
            
            response = requests.get(search_url, params=params)
            data = response.json()
            
            if not data['results']:
                print(f"❌ No results for '{movie_title}'")
                continue
            
            # Show search results if multiple
            results = data['results'][:5]
            if len(results) > 1:
                print(f"\nFound {len(data['results'])} results. Top matches:")
                for i, movie in enumerate(results, 1):
                    year = movie.get('release_date', '')[:4]
                    print(f"{i}. {movie['title']} ({year})")
                
                choice = input("Select number (or Enter for first result): ").strip()
                if choice.isdigit() and 1 <= int(choice) <= len(results):
                    selected_movie = results[int(choice) - 1]
                else:
                    selected_movie = results[0]
            else:
                selected_movie = results[0]
            
            movie_id = selected_movie['id']
            
            # Get detailed movie information
            movie_url = f"https://api.themoviedb.org/3/movie/{movie_id}"
            movie_params = {
                'api_key': API_KEY,
                'append_to_response': 'credits,release_dates'
            }
            
            movie_response = requests.get(movie_url, params=movie_params)
            movie_data = movie_response.json()
            
            # Add to DataFrame
            collector.add_movie_to_dataframe(movie_data)
            
            # Display movie info
            display_movie_info(movie_data)
            
        elif choice == '2':
            collector.display_dataset_info()
            
        elif choice == '3':
            collector.get_movie_statistics()
            
        elif choice == '4':
            filename = input("Enter base filename (or press Enter for 'movie_dataset'): ").strip()
            if not filename:
                filename = "movie_dataset"
            # Remove .csv extension if user added it
            if filename.endswith('.csv'):
                filename = filename[:-4]
            collector.save_to_csv(filename)
            
        elif choice == '5':
            # Ask if user wants to save before exiting
            if not collector.movies_df.empty:
                save = input("Save data before exiting? (y/n): ").strip().lower()
                if save == 'y':
                    collector.save_to_csv()
            print("Goodbye! 👋")
            break
        
        else:
            print("❌ Invalid option")

def display_movie_info(movie_data):
    """Display movie information"""
    credits_data = movie_data.get('credits', {})
    cast = credits_data.get('cast', [])[:10]
    
    directors = []
    for person in credits_data.get('crew', []):
        if person['job'] == 'Director':
            directors.append(person['name'])
    
    genres = [genre['name'] for genre in movie_data.get('genres', [])]
    release_date = movie_data.get('release_date', 'Unknown')
    runtime = movie_data.get('runtime', 'Unknown')
    
    print(f"\n🎬 {movie_data['title']} ({release_date[:4] if release_date != 'Unknown' else 'Unknown'})")
    print(f"⏱️  Runtime: {runtime} minutes" if runtime != 'Unknown' else "⏱️  Runtime: Unknown")
    
    if genres:
        print(f"🎭 Genres: {', '.join(genres)}")
    
    if directors:
        print(f"🎥 Director(s): {', '.join(directors)}")
    
    print("\n🌟 Main Cast (Top 10):")
    if cast:
        for i, actor in enumerate(cast, 1):
            print(f"   {i}. {actor['name']} as '{actor['character']}'")

# Run the interactive search
if __name__ == "__main__":
    interactive_movie_search()