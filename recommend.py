import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load cleaned dataset
df = pd.read_csv("data/movies_cleaned.csv")

# Rename columns
df.rename(columns={'title_x': 'title', 'title_y': 'title'}, inplace=True)

# Drop duplicate columns if necessary
df = df.loc[:, ~df.columns.duplicated()]

# Print the columns to check if 'title' exists
print("Columns in the dataset:", df.columns)

# Fill NaN values with empty strings
df['title'] = df['title'].fillna('')
df['overview'] = df['overview'].fillna('')
df['genres'] = df['genres'].fillna('')
df['keywords'] = df['keywords'].fillna('')

# Combine relevant features into a single string
df['combined_features'] = df['title'] + ' ' + df['genres'] + ' ' + df['overview'] + ' ' + df['keywords']

# Check for NaN values in combined_features
print("NaN values in combined_features:", df['combined_features'].isna().sum())

# TF-IDF Vectorizer for movie overview
tfidf = TfidfVectorizer(stop_words="english")
tfidf_matrix = tfidf.fit_transform(df['overview'].fillna(""))  # Convert text to vector

# Compute similarity scores
cosine_sim = cosine_similarity(tfidf_matrix)

print("\n✅ TF-IDF Matrix and Cosine Similarity computed successfully!")


# Function to get movie recommendations
def get_recommendations(title, df, cosine_sim):
    # Get movie index
    indices = pd.Series(df.index, index=df['title']).drop_duplicates()
    idx = indices.get(title, None)

    if idx is None:
        return ["Movie not found! Try another title."]

    # Get similarity scores for all movies
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:6]  # Top 5

    # Get recommended movie titles
    movie_indices = [i[0] for i in sim_scores]
    return df['title'].iloc[movie_indices].tolist()

# Test with an example
print("\n🎬 Recommended Movies:")
print(get_recommendations("aveng", df, cosine_sim))
