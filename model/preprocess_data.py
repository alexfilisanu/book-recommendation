import pandas as pd

books_df = pd.read_csv("../database/filtered_books.csv")
users_df = pd.read_csv("../database/filtered_users.csv")
ratings_df = pd.read_csv("../database/filtered_ratings.csv")

users_ratings_df = pd.merge(users_df, ratings_df, on='User-ID')
merged_df = pd.merge(users_ratings_df, books_df, on='ISBN')


def get_content_based_merged_df():
    df = merged_df.drop(columns=['Location', 'Age', 'Book-Title', 'Book-Author', 'Year-Of-Publication', 'Publisher', 'Image-URL-L'])
    return df
