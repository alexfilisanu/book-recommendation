import pickle

import pandas as pd
import numpy as np
import random
from sklearn.preprocessing import OneHotEncoder
from scipy.sparse.linalg import svds
from sklearn.metrics.pairwise import cosine_similarity
from math import sqrt
from sklearn.metrics import mean_squared_error, mean_absolute_error


books_df = pd.read_csv("../database/filtered_books.csv")
users_df = pd.read_csv("../database/filtered_users.csv")
ratings_df = pd.read_csv("../database/filtered_ratings.csv")

users_ratings_df = pd.merge(users_df, ratings_df, on='User-ID')
merged_df = pd.merge(users_ratings_df, books_df, on='ISBN')

user_item_matrix = merged_df.pivot_table(index='User-ID', columns='ISBN', values='Book-Rating').fillna(0)
user_item_matrix_values = user_item_matrix.values

U, sigma, Vt = svds(user_item_matrix_values, k=50)
sigma = np.diag(sigma)

predicted_ratings = np.dot(np.dot(U, sigma), Vt)

predicted_ratings_df = pd.DataFrame(predicted_ratings, index=user_item_matrix.index, columns=user_item_matrix.columns)

with open('../bookshelf/user_based_df.pkl', 'wb') as user_based_file:
    pickle.dump(predicted_ratings_df, user_based_file)

interactions_full_indexed_df = merged_df.set_index('User-ID')
ratings_train_df, ratings_test_df = np.split(ratings_df.sample(frac=1, random_state=42), [int(.8 * len(ratings_df))])
interactions_train_indexed_df = ratings_train_df.set_index('User-ID')
interactions_test_indexed_df = ratings_test_df.set_index('User-ID')

def get_items_interacted(user_id, interactions_df):
    interacted_items = interactions_df.loc[user_id]['ISBN']
    return set(interacted_items if type(interacted_items) == pd.Series else [interacted_items])

EVAL_RANDOM_SAMPLE_NON_INTERACTED_ITEMS = 100

def get_not_interacted_items_sample(user_id, sample_size, seed=42):
    interacted_items = get_items_interacted(user_id, interactions_full_indexed_df)
    all_items = set(books_df['ISBN'])
    non_interacted_items = all_items - interacted_items

    random.seed(seed)
    sample_size = min(sample_size, len(non_interacted_items))  # Adjust sample size
    non_interacted_items_sample = random.sample(list(non_interacted_items), sample_size)
    return set(non_interacted_items_sample)

def _verify_hit_top_n(item_id, recommended_items, topn):
    try:
        index = next(i for i, c in enumerate(recommended_items) if c == item_id)
    except StopIteration:
        index = -1
    hit = int(index in range(0, topn))
    return hit, index

def evaluate_model_for_user(model, user_id):
    interacted_values_testset = interactions_test_indexed_df.loc[user_id]
    if type(interacted_values_testset['ISBN']) == pd.Series:
        user_interacted_items_testset = set(interacted_values_testset['ISBN'])
    else:
        user_interacted_items_testset = {interacted_values_testset['ISBN']}

    interacted_items_count_testset = len(user_interacted_items_testset)

    user_ratings = predicted_ratings_df.loc[user_id].sort_values(ascending=False)
    hits_at_5_count = 0
    hits_at_10_count = 0

    for item_id in user_interacted_items_testset:
        non_interacted_items_sample = get_not_interacted_items_sample(user_id, sample_size=EVAL_RANDOM_SAMPLE_NON_INTERACTED_ITEMS, seed=hash(item_id)%(2**32))
        items_to_filter_recs = non_interacted_items_sample.union({item_id})
        valid_recs = user_ratings[user_ratings.index.isin(items_to_filter_recs)].index.tolist()

        hit_at_5, index_at_5 = _verify_hit_top_n(item_id, valid_recs, 5)
        hits_at_5_count += hit_at_5
        hit_at_10, index_at_10 = _verify_hit_top_n(item_id, valid_recs, 10)
        hits_at_10_count += hit_at_10

    recall_at_5 = hits_at_5_count / float(interacted_items_count_testset)
    recall_at_10 = hits_at_10_count / float(interacted_items_count_testset)

    user_metrics = {'hits@5_count': hits_at_5_count,
                    'hits@10_count': hits_at_10_count,
                    'interacted_count': interacted_items_count_testset,
                    'recall@5': recall_at_5,
                    'recall@10': recall_at_10}
    return user_metrics

def evaluate_model(model):
    users_metrics = []
    for idx, user_id in enumerate(list(interactions_test_indexed_df.index.unique().values)):
        user_metrics = evaluate_model_for_user(model, user_id)
        user_metrics['_user_id'] = user_id
        users_metrics.append(user_metrics)

    print('%d users processed' % idx)

    detailed_results_df = pd.DataFrame(users_metrics).sort_values('interacted_count', ascending=False)

    global_recall_at_5 = detailed_results_df['hits@5_count'].sum() / float(detailed_results_df['interacted_count'].sum())
    global_recall_at_10 = detailed_results_df['hits@10_count'].sum() / float(detailed_results_df['interacted_count'].sum())

    global_metrics = {'modelName': 'Collaborative Filtering (SVD)',
                      'recall@5': global_recall_at_5,
                      'recall@10': global_recall_at_10}

    return global_metrics, detailed_results_df

cf_global_metrics, cf_detailed_results_df = evaluate_model(predicted_ratings_df)

print('\nGlobal metrics:\n%s' % cf_global_metrics)
def preprocess_books_df(books_df):
    categorical_columns = ['Book-Author', 'Publisher', 'Year-Of-Publication']
    encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
    encoded_features = pd.DataFrame(encoder.fit_transform(books_df[categorical_columns]),
                                    columns=encoder.get_feature_names_out(categorical_columns),
                                    index=books_df.index)

    numerical_columns = books_df.select_dtypes(include=['number'])
    preprocessed_df = pd.concat([numerical_columns, encoded_features], axis=1)

    preprocessed_df = preprocessed_df.fillna(0)
    return preprocessed_df

def calculate_diversity(recommended_items_df, books_df):
    book_features = preprocess_books_df(books_df)
    book_features = book_features.set_index(books_df['ISBN'])

    item_similarity_matrix = cosine_similarity(book_features)
    np.fill_diagonal(item_similarity_matrix, 0)

    total_similarity = 0
    total_pairs = 0

    for user_id in recommended_items_df.index:
        recommended_items = recommended_items_df.loc[user_id].nlargest(10).index
        pairs = [(item1, item2) for item1 in recommended_items for item2 in recommended_items if item1 != item2]
        for item1, item2 in pairs:
            item1_idx = book_features.index.get_loc(item1)
            item2_idx = book_features.index.get_loc(item2)
            total_similarity += item_similarity_matrix[item1_idx, item2_idx]
            total_pairs += 1
    print(total_pairs)
    return 1 - (total_similarity / total_pairs if total_pairs > 0 else 1)

overall_diversity = calculate_diversity(predicted_ratings_df, books_df)
print(f'Overall Diversity: {overall_diversity:.4f}')

def calculate_rmse_mae(predicted_ratings_df, interactions_test_indexed_df):
    actual_ratings = []
    predicted_ratings = []

    for user_id in interactions_test_indexed_df.index.unique():
        if user_id in predicted_ratings_df.index:
            user_actual_ratings = interactions_test_indexed_df.loc[user_id]
            if type(user_actual_ratings) == pd.Series:
                user_actual_ratings = pd.DataFrame(user_actual_ratings).T

            for index, row in user_actual_ratings.iterrows():
                isbn = row['ISBN']
                actual_rating = row['Book-Rating']

                if isbn in predicted_ratings_df.columns:
                    predicted_rating = predicted_ratings_df.loc[user_id, isbn]
                    actual_ratings.append(actual_rating)
                    predicted_ratings.append(predicted_rating)

    rmse = sqrt(mean_squared_error(actual_ratings, predicted_ratings))
    mae = mean_absolute_error(actual_ratings, predicted_ratings)
    return rmse, mae

rmse, mae = calculate_rmse_mae(predicted_ratings_df, interactions_test_indexed_df)
print(f'RMSE: {rmse:.4f}')
print(f'MAE: {mae:.4f}')