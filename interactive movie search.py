import requests

API_KEY = "fabd38ebf81a46886c7230f8cd265f04"

def interactive_movie_search():
    while True:
        print("\n" + "🎬" * 20)
        movie_title = input("Enter movie title (or 'quit' to exit): ").strip()
        
        if movie_title.lower() == 'quit':
            break
            
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
        results = data['results'][:5]  # Show top 5 results
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
        
        # Get cast for selected movie
        movie_id = selected_movie['id']
        credits_url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits"
        credits_response = requests.get(credits_url, params={'api_key': API_KEY})
        credits_data = credits_response.json()
        
        cast = credits_data.get('cast', [])[:10]
        
        print(f"\n🎬 {selected_movie['title']} ({selected_movie.get('release_date', '')[:4]})")
        print("🌟 Main Cast:")
        for i, actor in enumerate(cast, 1):
            print(f"   {i}. {actor['name']} as '{actor['character']}'")

# Run the interactive search
interactive_movie_search()