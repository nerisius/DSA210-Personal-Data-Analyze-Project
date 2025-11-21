from dotenv import load_dotenv
import requests
import pandas as pd
from datetime import datetime
import os

load_dotenv()
# Load API keys
API_KEY = os.getenv('TMDB_API_KEY') 
OMDB_KEY = os.getenv('OMDB_API_KEY') 


def get_omdb_data(title, year=None, omdb_api_key=None):
    """Fetch ratings from OMDb API"""
    if not omdb_api_key:
        print("⚠️ OMDb API key not provided, skipping ratings")
        return None
    
    params = {
        "t": title,
        "apikey": omdb_api_key
    }
    # Only add year if it's valid (4 digits)
    if year and year != 'Unknown' and len(str(year)) == 4:
        params["y"] = year

    try:
        response = requests.get("http://www.omdbapi.com/", params=params, timeout=5)
        data = response.json()

        if data.get("Response") == "False":
            print(f"   ℹ️ OMDb: No match found for '{title}' ({year})")
            return None

        # Extract ratings
        imdb = data.get("imdbRating", "N/A")
        if imdb == "N/A":
            imdb = None
            
        rt = None
        for r in data.get("Ratings", []):
            if r["Source"] == "Rotten Tomatoes":
                rt = r["Value"]

        print(f"   ✓ OMDb: Found ratings - IMDb: {imdb}, RT: {rt}")
        return {
            "imdb_rating": imdb,
            "rt_rating": rt,
        }
    except Exception as e:
        print(f"   ⚠️ Error fetching OMDb data: {e}")
        return None


class MovieDataCollector:
    def __init__(self, filename="movie_dataset.csv"):
        self.filename = filename

        # If CSV exists → load it
        if os.path.exists(filename):
            print(f"📂 Existing dataset found. Loading {filename}...")
            self.movies_df = pd.read_csv(filename)

            # Add new columns if they don't exist
            if 'imdb_rating' not in self.movies_df.columns:
                self.movies_df['imdb_rating'] = None
                print("   Added 'imdb_rating' column")
            
            if 'rt_rating' not in self.movies_df.columns:
                self.movies_df['rt_rating'] = None
                print("   Added 'rt_rating' column")

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
                'countries', 'imdb_rating', 'rt_rating', 'collection_date'
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

        # Cast (top 10)
        cast = [actor['name'] for actor in movie_data.get('credits', {}).get('cast', [])[:10]]

        # Countries
        countries = [c['name'] for c in movie_data.get('production_countries', [])]

        # Timestamp
        collection_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        structured_data = {
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
        
        # Fetch OMDb data
        print(f"   🔍 Fetching OMDb ratings for '{title}'...")
        omdb_data = get_omdb_data(
            title=structured_data['title'],
            year=structured_data['release_year'],
            omdb_api_key=OMDB_KEY
        )
        
        # Add OMDb data if available
        if omdb_data:
            structured_data.update(omdb_data)
        else:
            # Add None values if OMDb data not found
            structured_data['imdb_rating'] = None
            structured_data['rt_rating'] = None

        return structured_data

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



    def update_missing_ratings(self):
        """Update movies that are missing IMDb or RT ratings"""
        if self.movies_df.empty:
            print("❌ No movies in dataset.")
            return
        
        # Find movies missing ratings
        missing_ratings = self.movies_df[
            self.movies_df['imdb_rating'].isna() | self.movies_df['rt_rating'].isna()
        ]
        
        if missing_ratings.empty:
            print("✅ All movies already have ratings!")
            return
        
        print(f"\n🔄 Found {len(missing_ratings)} movies missing ratings.")
        print("Fetching ratings...\n")
        
        updated_count = 0
        for idx, row in missing_ratings.iterrows():
            title = row['title']
            year = row['release_year']
            
            print(f"Processing: {title} ({year})")
            omdb_data = get_omdb_data(title, year, OMDB_KEY)
            
            if omdb_data:
                self.movies_df.at[idx, 'imdb_rating'] = omdb_data.get('imdb_rating')
                self.movies_df.at[idx, 'rt_rating'] = omdb_data.get('rt_rating')
                updated_count += 1
            else:
                # Set to None if still not found
                self.movies_df.at[idx, 'imdb_rating'] = None
                self.movies_df.at[idx, 'rt_rating'] = None
        
        print(f"\n✅ Updated {updated_count} movies with ratings.")
        
        # Ask to save
        save = input("\nSave changes to CSV? (y/n): ").strip().lower()
        if save == 'y':
            self.save_to_csv()

######################################################################################################################################

    def import_letterboxd_csv(csv_path, collector):
        """Automatically import movies from Letterboxd export CSV."""
        df = pd.read_csv(csv_path)

        # Basic checks
        if 'Name' not in df.columns or 'Year' not in df.columns:
            print("❌ CSV must contain 'Name' and 'Year' columns.")
            return

        for idx, row in df.iterrows():
            title = row['Name']
            year = str(row['Year'])

            print(f"\n📌 Processing [{idx+1}/{len(df)}] {title} ({year})")

            # TMDB search
            search_url = "https://api.themoviedb.org/3/search/movie"
            params = {'api_key': API_KEY, 'query': title, 'Year': year}

            response = requests.get(search_url, params=params)
            data = response.json()

            # Handle no results
            if not data.get('results'):
                print(f"❌ No TMDB result for '{title}' ({year})")
                continue

            # Take first match
            selected_movie = data['results'][0]
            movie_id = selected_movie['id']

            # Fetch details
            movie_url = f"https://api.themoviedb.org/3/movie/{movie_id}"
            movie_params = {
                'api_key': API_KEY,
                'append_to_response': 'credits'
            }

            movie_response = requests.get(movie_url, params=movie_params)
            movie_data = movie_response.json()

            # Add to dataset
            collector.add_movie_to_dataframe(movie_data)

        print("\n🎉 Import complete!")
        collector.save_to_csv()


    ###############################################################################################################################



def display_movie_info(movie_data):
    credits = movie_data.get('credits', {})

    directors = [p['name'] for p in credits.get('crew', []) if p.get('job') == 'Director']
    genres = [g['name'] for g in movie_data.get('genres', [])]

    release_date = movie_data.get('release_date', 'Unknown')

    print(f"\n {movie_data['title']} ({release_date[:4] if release_date != 'Unknown' else 'Unknown'})")
    print(f" Directors: {', '.join(directors)}")



def interactive_movie_search():
    collector = MovieDataCollector()

    while True:
        print("\n" + "*" * 20)
        print("1. Search for a movie")
        print("2. Save dataset")
        print("3. Import Letterboxd CSV")
        print("4. Update missing IMDb/RT ratings")   
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
            collector.save_to_csv()

        elif choice == '3':
            csv_path = input("Enter Letterboxd CSV path: ").strip()
            if os.path.exists(csv_path):
               import_letterboxd_csv(csv_path, collector)
            else:
               print("❌ File not found.")    


        elif choice == '4':  # <-- handle the new option
            collector.update_missing_ratings()       

        elif choice == '5':
            if not collector.movies_df.empty:
                save = input("Save before exit? (y/n): ").strip().lower()
                if save == 'y':
                    collector.save_to_csv()

            print("Goodbye!")
            break

        else:
            print("Invalid option.")


if __name__ == "__main__":
    interactive_movie_search()