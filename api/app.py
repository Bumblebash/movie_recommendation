from flask import Flask, request, jsonify
from src.scraper.imdb_scraper import scrape_movies
from src.scraper.mappings import EMOTION_TO_GENRE

app = Flask(__name__)

@app.route('/recommend', methods=['GET'])
def recommend():
    """API endpoint to get movie recommendations based on emotion."""
    emotion = request.args.get('emotion', '').capitalize()
    genre = EMOTION_TO_GENRE.get(emotion)

    if not genre:
        return jsonify({"error": "Invalid emotion"}), 400

    movies = scrape_movies(genre)
    return jsonify({"emotion": emotion, "genre": genre, "movies": movies})

if __name__ == '__main__':
    app.run(debug=True)
