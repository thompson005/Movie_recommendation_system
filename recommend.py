import requests
import random

# Replace 'YOUR_API_KEY' with your TMDb API key
api_key = '132d9d712f1e4b9b45d09150d03934fe'

# Function to search for a movie by title
def search_movie_by_title(title):
    endpoint = 'https://api.themoviedb.org/3/search/movie'
    params = {'api_key': api_key, 'language': 'en-US', 'query': title, 'page': 1}
    response = requests.get(endpoint, params=params)
    data = response.json()
    return data['results']

# Function to recommend a movie from the same genre
def recommend_movie_from_same_genre(movie_data):
    if not movie_data:
        return "Movie not found. Please try another title."

    # Select the first movie in the search results
    selected_movie = movie_data[0]
    selected_genre_ids = selected_movie.get('genre_ids', [])

    # Now, let's find other movies with the same genre
    endpoint = 'https://api.themoviedb.org/3/discover/movie'
    params = {
        'api_key': api_key,
        'language': 'en-US',
        'with_genres': ",".join(map(str, selected_genre_ids)),
        'page': 1
    }
    response = requests.get(endpoint, params=params)
    data = response.json()

    if data.get('results'):
        recommended_movies = data['results']
        if recommended_movies:
            random_movie = random.choice(recommended_movies)
            return random_movie['title']

    return "No similar movies found for the selected genre."

if __name__ == "__main__":
    user_input = input("Enter a movie title: ")
    movie_data = search_movie_by_title(user_input)

    recommended_movie = recommend_movie_from_same_genre(movie_data)
    print("Recommended Movie (Same Genre):", recommended_movie)
