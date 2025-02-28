import pandas as pd
import json

# Load Movies Dataset with error handling
try:
    movies_df = pd.read_csv("data/movies.csv", delimiter=',', quotechar='"', quoting=1, on_bad_lines='skip')
    print("✅ Movies data loaded successfully!")
except pd.errors.ParserError as e:
    print(f"❌ Error loading movies data: {e}")

# Load Credits Dataset
credits_df = pd.read_csv("data/credits.csv")

# Display DataFrames
print("Movies Data:")
print(movies_df.head())

print("\nCredits Data:")
print(credits_df.head())

# Check if 'movie_id' column exists in both DataFrames
print("\nColumns in movies_df:", movies_df.columns)
print("Columns in credits_df:", credits_df.columns)

if 'movie_id' in movies_df.columns:
    print("✅ 'movie_id' column exists in movies_df")

# Ensure 'movie_id' column is of the same data type in both DataFrames
movies_df['movie_id'] = movies_df['movie_id'].astype(str)
credits_df['movie_id'] = credits_df['movie_id'].astype(str)

# Merge movies.csv with credits.csv using movie_id
if 'movie_id' in movies_df.columns and 'movie_id' in credits_df.columns:
    movies_merged_df = movies_df.merge(credits_df, on="movie_id", how="left")
    print("✅ Merged movies_df with credits_df!")

    # Save the merged dataset to a CSV file
    movies_merged_df.to_csv("data/movies_merged.csv", index=False)
    print("✅ Merged dataset saved to 'data/movies_merged.csv'")

    # Load the merged dataset
    merged_df = pd.read_csv("data/movies_merged.csv")

    # Handle missing values (fill or drop them)
    merged_df.fillna('', inplace=True)

    # Convert JSON-like columns into readable format
    def parse_json_column(column):
        return column.apply(lambda x: json.loads(x.replace("'", '"')) if x else [])

    merged_df['cast'] = parse_json_column(merged_df['cast'])
    merged_df['crew'] = parse_json_column(merged_df['crew'])

  
    cleaned_df = merged_df

    # Save the cleaned dataset
    cleaned_df.to_csv("data/movies_cleaned.csv", index=False)
    print("✅ Cleaned dataset saved to 'data/movies_cleaned.csv'")

    # Display the cleaned dataset
    print("\nCleaned Dataset:")
    print(cleaned_df.head())
else:
    print("❌ Cannot merge DataFrames due to missing 'movie_id' column.")