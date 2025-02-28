import pandas as pd

# Load cleaned dataset
df = pd.read_csv("data/movies_merged.csv")

# Rename columns
df.rename(columns={'title_x': 'title', 'title_y': 'title'}, inplace=True)

# Drop duplicate columns if necessary
df = df.loc[:, ~df.columns.duplicated()]

# Print the first 20 titles to verify the exact format
print("Titles in the dataset:")
print(df['title'].head(20))