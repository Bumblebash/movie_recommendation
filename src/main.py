from src.scraper.imdb_scraper import scrape_movies
from src.scraper.mappings import EMOTION_TO_GENRE

def main():
    """CLI-based movie recommendation system."""
    emotion = input("Enter your emotion: ").capitalize()
    genre = EMOTION_TO_GENRE.get(emotion)

    if not genre:
        print("Invalid emotion.")
        return

    movies = scrape_movies(genre)
    print(f"\nTop 5 {genre} movies recommended for {emotion} emotion:")
    for i, title in enumerate(movies, 1):
        print(f"{i}. {title}")

if __name__ == '__main__':
    main()
