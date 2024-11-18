import pandas as pd

books_df = pd.read_csv("books.csv")
ratings_df = pd.read_csv("ratings.csv")
users_df = pd.read_csv("users.csv")

isbn_counts = ratings_df['ISBN'].value_counts()
popular_books = isbn_counts[isbn_counts > 50].index

filtered_books_df = books_df[books_df['ISBN'].isin(popular_books)]
filtered_ratings_df = ratings_df[ratings_df['ISBN'].isin(popular_books)]

valid_user_ids = filtered_ratings_df['User-ID'].unique()
filtered_users_df = users_df[users_df['User-ID'].isin(valid_user_ids)]

filtered_books_df.to_csv("filtered_books.csv", index=False)
filtered_ratings_df.to_csv("filtered_ratings.csv", index=False)
filtered_users_df.to_csv("filtered_users.csv", index=False)
