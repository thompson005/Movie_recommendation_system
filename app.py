from flask import Flask, render_template, request
import requests
import random

app = Flask(__name__)

# Replace 'YOUR_TMDB_API_KEY' with your TMDb API key
tmdb_api_key = '132d9d712f1e4b9b45d09150d03934fe'

# Function to get director information for a movie
def get_directors(tmdb_id):
    url = f"https://api.themoviedb.org/3/movie/{tmdb_id}?api_key={tmdb_api_key}&append_to_response=credits"
    response = requests.get(url)
    data = response.json()
    
    if 'credits' in data:
        crew = data['credits']['crew']
        directors = [member['name'] for member in crew if member['job'] == 'Director']
        return directors
    else:
        return []

# Function to recommend movies by the same directors
def recommend_movies_by_directors(movie_title):
    # Search for a movie by title
    search_url = f"https://api.themoviedb.org/3/search/movie?api_key={tmdb_api_key}&language=en-US&query={movie_title}&page=1"
    response = requests.get(search_url)
    data = response.json()
    
    if 'results' in data and data['results']:
        selected_movie = data['results'][0]
        movie_id = selected_movie['id']
        director_names = get_directors(movie_id)
        
        recommended_movies = []

        if director_names:
            for director_name in director_names:
                director_search_url = f"https://api.themoviedb.org/3/search/person?api_key={tmdb_api_key}&query={director_name}&page=1"
                director_response = requests.get(director_search_url)
                director_data = director_response.json()
                
                if 'results' in director_data and director_data['results']:
                    director_id = director_data['results'][0]['id']
                    director_movies_url = f"https://api.themoviedb.org/3/person/{director_id}/movie_credits?api_key={tmdb_api_key}"
                    director_movies_response = requests.get(director_movies_url)
                    director_movies_data = director_movies_response.json()

                    if 'cast' in director_movies_data:
                        director_movies = director_movies_data['cast']
                        recommended_movies.extend(director_movies)

        # Randomly select up to 3 recommended movies
        recommended_movies = random.sample(recommended_movies, min(3, len(recommended_movies)))
        return selected_movie, recommended_movies

# Flask routes
@app.route("/", methods=["GET", "POST"])
def index():
    user_input = None
    selected_movie = None
    recommended_movies = []

    if request.method == "POST":
        user_input = request.form.get("movie_title")
        selected_movie, recommended_movies = recommend_movies_by_directors(user_input)

    return render_template("index.html", user_input=user_input, selected_movie=selected_movie, recommended_movies=recommended_movies)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
