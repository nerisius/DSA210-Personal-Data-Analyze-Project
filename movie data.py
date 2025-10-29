import requests
import pandas as pd
from datetime import datetime
import os

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
        
        # Extract cast with character information
        cast = []
        for actor in credits_data.get('cast', [])[:15]:  # Top 15 cast members
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
    
    def save_to_csv(self, filename="movie_dataset.csv"):
        """Save DataFrame to CSV file"""
        if not self.movies_df.empty:
            self.movies_df.to_csv(filename, index=False)
            print(f"💾 Data saved to {filename}")
            return True
        else:
            print("❌ No data to save")
            return False
    
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
        print(f"   Average runtime: {self.movies_df['runtime'].mean():.2f} minutes")
        
        # Genre frequency
        all_genres = [genre for sublist in self.movies_df['genres'] for genre in sublist]
        genre_counts = pd.Series(all_genres).value_counts()
        print(f"   Most common genre: {genre_counts.index[0] if not genre_counts.empty else 'N/A'}")
        
        # Director frequency
        all_directors = [director for sublist in self.movies_df['directors'] for director in sublist]
        director_counts = pd.Series(all_directors).value_counts()
        if not director_counts.empty:
            print(f"   Most frequent director: {director_counts.index[0]} ({director_counts.iloc[0]} movies)")


##################################################################################################################################################
def interactive_movie_search():
    collector = MovieDataCollector()
    
    while True:
        print("\n" + "🎬" * 20)
        print("1. Search for a movie")
        print("2. Show dataset info")
        print("3. Show statistics")
        print("4. Save to CSV")
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
            filename = input("Enter filename (or press Enter for 'movie_dataset.csv'): ").strip()
            if not filename:
                filename = "movie_dataset.csv"
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
    """Display movie information (similar to your original function)"""
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
    
    print("\n🌟 Main Cast:")
    if cast:
        for i, actor in enumerate(cast, 1):
            print(f"   {i}. {actor['name']} as '{actor['character']}'")

# Run the interactive search
if __name__ == "__main__":
    interactive_movie_search()