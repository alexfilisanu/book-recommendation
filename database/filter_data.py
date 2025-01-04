import pandas as pd

books_df = pd.read_csv("books.csv")
ratings_df = pd.read_csv("ratings.csv")
users_df = pd.read_csv("users.csv")

# Remove unnecessary columns from books_df
books_df.drop(columns=['Image-URL-S', 'Image-URL-M'], inplace=True)

# Remove ratings with 0
ratings_df = ratings_df[ratings_df['Book-Rating'] != 0]

# Keep only books with more than 50 reviews
isbn_counts = ratings_df['ISBN'].value_counts()
popular_books = isbn_counts[isbn_counts > 50].index
filtered_books_df = books_df[books_df['ISBN'].isin(popular_books)]
filtered_ratings_df = ratings_df[ratings_df['ISBN'].isin(popular_books)]

# Keep only users that reviewed more than 20 books
user_review_counts = filtered_ratings_df['User-ID'].value_counts()
active_users = user_review_counts[user_review_counts > 20].index
filtered_ratings_df = filtered_ratings_df[filtered_ratings_df['User-ID'].isin(active_users)]
filtered_users_df = users_df[users_df['User-ID'].isin(active_users)]

filtered_books_df.to_csv("filtered_books.csv", index=False)
filtered_ratings_df.to_csv("filtered_ratings.csv", index=False)
filtered_users_df.to_csv("filtered_users.csv", index=False)
