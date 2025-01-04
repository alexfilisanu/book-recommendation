import pickle

from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
import pandas as pd

books_df = pd.read_csv("../database/filtered_books.csv")
users_df = pd.read_csv("../database/filtered_users.csv")
ratings_df = pd.read_csv("../database/filtered_ratings.csv")

users_ratings_df = pd.merge(users_df, ratings_df, on='User-ID')
merged_df = pd.merge(users_ratings_df, books_df, on='ISBN')

merged_df = merged_df.drop(
    columns=['Location', 'Age', 'Book-Title', 'Book-Author', 'Year-Of-Publication', 'Publisher', 'Image-URL-L']
)

train_data, test_data = train_test_split(merged_df, test_size=0.2, random_state=42)

pivot_data = train_data # Replace with merged_df to train the model better for creating the blended_similarity.pkl
pivot_table = pd.pivot_table(train_data, index='User-ID', columns='ISBN', values='Book-Rating').fillna(0)
book_user_matrix = pivot_table.T

n_components = 50
svd = TruncatedSVD(n_components=n_components)
latent_factors = svd.fit_transform(book_user_matrix)
similarity_matrix = cosine_similarity(latent_factors)
similarity_df = pd.DataFrame(similarity_matrix, index=book_user_matrix.index, columns=book_user_matrix.index)

def recommend_books_svd(book_id, n_recommendations=5):
    if book_id not in similarity_df.index:
        print(f"Book {book_id} not found in the dataset.")
        return []
    similar_books = similarity_df[book_id].sort_values(ascending=False)[1:n_recommendations + 1]
    recommendations = [
        (isbn, books_df[books_df['ISBN'] == isbn]['Book-Title'].values[0], score)
        for isbn, score in similar_books.items()
    ]
    return recommendations

books_df['Metadata'] = books_df['Book-Title'] + " " + books_df['Book-Author']
tfidf_vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf_vectorizer.fit_transform(books_df['Metadata'])

metadata_similarity = cosine_similarity(tfidf_matrix, tfidf_matrix)
metadata_similarity_df = pd.DataFrame(metadata_similarity, index=books_df['ISBN'], columns=books_df['ISBN'])

alpha = 0.7
blended_similarity = alpha * similarity_matrix + (1 - alpha) * metadata_similarity_df.values
blended_similarity_df = pd.DataFrame(blended_similarity, index=book_user_matrix.index, columns=book_user_matrix.index)
with open('../bookshelf/blended_similarity.pkl', 'wb') as blended_file:
    pickle.dump(blended_similarity_df, blended_file)

def recommend_books_hybrid(book_id, n_recommendations=5):
    if book_id not in blended_similarity_df.index:
        print(f"Book {book_id} not found in the dataset.")
        return []
    similar_books = blended_similarity_df[book_id].sort_values(ascending=False)[1:n_recommendations + 1]
    recommendations = [
        (isbn, books_df[books_df['ISBN'] == isbn]['Book-Title'].values[0], score)
        for isbn, score in similar_books.items()
    ]
    return recommendations

print("Top recommendations for the book using Hybrid Approach:")
book_id = "0439139597"
hybrid_recommendations = recommend_books_hybrid(book_id)
for isbn, title, score in hybrid_recommendations:
    print(f"ISBN: {isbn}, Title: {title}, Similarity: {score}")

def evaluate_precision_recall(test_data, recommend_function, n_recommendations=10):
    hits = 0
    total_relevant = 0
    total_recommended = 0

    test_users = test_data['User-ID'].unique()

    for user in test_users:
        user_books = test_data[(test_data['User-ID'] == user) & (test_data['Book-Rating'] > 5)]['ISBN'].tolist()

        if not user_books:
            continue

        target_book = user_books[0]
        recommendations = recommend_function(target_book, n_recommendations)

        if recommendations:
            recommended_books = [rec[0] for rec in recommendations]
            hits += len(set(recommended_books) & set(user_books))

            total_recommended += len(recommended_books)
            total_relevant += len(user_books)

    precision = hits / total_recommended if total_recommended > 0 else 0
    recall = hits / total_relevant if total_relevant > 0 else 0
    return precision, recall


precision_svd, recall_svd = evaluate_precision_recall(test_data, recommend_books_svd)
print(f"SVD Recommendations - Precision: {precision_svd:.4f}, Recall: {recall_svd:.4f}")

precision_hybrid, recall_hybrid = evaluate_precision_recall(test_data, recommend_books_hybrid)
print(f"Hybrid Recommendations - Precision: {precision_hybrid:.4f}, Recall: {recall_hybrid:.4f}")
