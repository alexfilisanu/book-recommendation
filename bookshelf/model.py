import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
import matplotlib.pyplot as plt
import seaborn as sns
import pickle

books = pd.read_csv("../database/filtered_books.csv", sep=',', encoding="latin-1", low_memory=False, on_bad_lines='skip', encoding_errors='replace')
users = pd.read_csv("../database/filtered_users.csv", sep=',', encoding="latin-1", low_memory=False, on_bad_lines='skip', encoding_errors='replace')
ratings = pd.read_csv("../database/filtered_ratings.csv", sep=',', encoding="latin-1", low_memory=False, on_bad_lines='skip', encoding_errors='replace')

x = ratings['User-ID'].value_counts() > 200
y = x[x].index
ratings = ratings[ratings['User-ID'].isin(y)]
rating_with_books = ratings.merge(books, on='ISBN')

number_rating = rating_with_books.groupby('Book-Title')['Book-Rating'].count().reset_index()
number_rating.rename(columns= {'Book-Rating':'Number-of-Ratings'}, inplace=True)
final_rating = rating_with_books.merge(number_rating, on='Book-Title')
final_rating = final_rating[final_rating['Number-of-Ratings'] >= 50]
final_rating.drop_duplicates(['User-ID','Book-Title'], inplace=True)

book_pivot = final_rating.pivot_table(columns='User-ID', index='Book-Title', values="Book-Rating")
book_pivot.fillna(0, inplace=True)

book_sparse = csr_matrix(book_pivot)

book_pivot.to_pickle("book_pivot.pkl")

# Train and save model
book_sparse = csr_matrix(book_pivot)
model = NearestNeighbors(algorithm='brute')
model.fit(book_sparse)
with open("../../etapa1/model.pkl", "wb") as f:
    pickle.dump(model, f)

distances, suggestions = model.kneighbors(book_pivot.iloc[237, :].values.reshape(1, -1))
print(book_pivot.iloc[237, :])
target_book = book_pivot.index[237]
print(f"Recommendations for '{target_book}':")
for i in range(1, len(suggestions[0])):
    print(f"{i}: {book_pivot.index[suggestions[0][i]]}")

filtered_books = final_rating[final_rating['Book-Rating'] > 0]

# # Distributia de rating-uri
# plt.figure(figsize=(12, 6))
# sns.histplot(filtered_books['Book-Rating'], bins=10, kde=True)
# plt.xlabel('Book Rating')
# plt.ylabel('Frequency')
# plt.title('Distribution of Book Ratings')
# plt.show()

# # Topul cartilor cu cele mai mare numar de rating-uri
# top_books = filtered_books['Book-Title'].value_counts().head(10)
# plt.figure(figsize=(12, 6))
# top_books.index = top_books.index.map(lambda x: '\n'.join(textwrap.wrap(x, width=20)))
# top_books.plot(kind='barh')
# plt.xlabel('Number of Ratings')
# plt.title('Top 10 Books by Number of Ratings')
# plt.gca().invert_yaxis()
# plt.show()

# # Topul celor mai bine apreciate carti(dupa medie rating-ului)
# top_rated_books = filtered_books.groupby('Book-Title')['Book-Rating'].mean().nlargest(10)
# plt.figure(figsize=(12, 6))
# top_rated_books.index = top_rated_books.index.map(lambda x: '\n'.join(textwrap.wrap(x, width=20)))
# top_rated_books.plot(kind='barh')
# plt.xlabel('Average Rating')
# plt.title('Top 10 Rated Books')
# plt.gca().invert_yaxis()
# plt.show()

# # Distributia de carti apreciate per utilizator
# user_activity = ratings['User-ID'].value_counts()
# plt.figure(figsize=(10, 5))
# # sns.histplot(user_activity[user_activity > 2000], bins=100)
# sns.histplot(user_activity[user_activity > 200], bins=100)
# plt.title('Distribution of User Rating Counts')
# plt.xlabel('Number of Ratings per User')
# plt.ylabel('Number of Users')
# plt.show()
