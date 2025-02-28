from flask import Flask, request, render_template
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Load cleaned dataset
df = pd.read_csv("data/movies_cleaned.csv")

# Rename columns
df.rename(columns={'title_x': 'title', 'title_y': 'title'}, inplace=True)

# Drop duplicate columns if necessary
df = df.loc[:, ~df.columns.duplicated()]

# Fill NaN values with empty strings
df['title'] = df['title'].fillna('')
df['overview'] = df['overview'].fillna('')
df['genres'] = df['genres'].fillna('')
df['keywords'] = df['keywords'].fillna('')
df['vote_average'] = df['vote_average'].fillna(0)
df['popularity'] = df['popularity'].fillna(0)

# Combine relevant features into a single string
df['combined_features'] = df['title'] + ' ' + df['genres'] + ' ' + df['overview'] + ' ' + df['keywords']

# TF-IDF Vectorizer for combined features
tfidf = TfidfVectorizer(stop_words="english")
tfidf_matrix = tfidf.fit_transform(df['combined_features'])

# Compute similarity scores
cosine_sim = cosine_similarity(tfidf_matrix)

# Function to get movie recommendations
def get_recommendations(title, df, cosine_sim, top_n=10):
    # Get movie index
    indices = pd.Series(df.index, index=df['title']).drop_duplicates()
    idx = indices.get(title, None)

    if idx is None:
        return ["Movie not found! Try another title."]

    # Get similarity scores for all movies
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the top_n most similar movies
    sim_scores = sim_scores[1:top_n+1]

    # Get the movie indices
    movie_indices = [i[0] for i in sim_scores]

    # Get the recommended movies
    recommended_movies = df.iloc[movie_indices]

    # Incorporate user preferences (ratings and popularity)
    recommended_movies['score'] = recommended_movies['vote_average'] * 0.5 + recommended_movies['popularity'] * 0.5
    recommended_movies = recommended_movies.sort_values('score', ascending=False)

    return recommended_movies['title'].tolist()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    title = request.form['title']
    recommendations = get_recommendations(title, df, cosine_sim)
    return render_template('index.html', recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)