import requests
from bs4 import BeautifulSoup
import csv
import re

# IMDb URL for Top Rated Movies
URL = "https://www.imdb.com/chart/top/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def scrape_imdb():
    """Scrapes top-rated movies from IMDb and saves to CSV."""
    try:
        response = requests.get(URL, headers=HEADERS)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return
    
    soup = BeautifulSoup(response.text, "html.parser")
    movies = []

    for item in soup.select(".lister-list tr"):  # Selecting movie rows
        title = item.select_one(".titleColumn a").get_text()
        year = item.select_one(".titleColumn span").get_text(strip=True).strip("()")
        rating = item.select_one(".imdbRating strong").get_text()
        movies.append([title, year, rating])
    
    save_to_csv(movies)
    print("Scraping completed! Data saved to movies.csv")

def save_to_csv(movies):
    """Saves scraped movie data to a CSV file."""
    with open("movies.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Title", "Year", "Rating"])  # Column headers
        writer.writerows(movies)

if __name__ == "__main__":
    scrape_imdb()
