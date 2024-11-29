import pickle
from pandas import pivot_table
from sklearn.neighbors import NearestNeighbors

from model.preprocess_data import get_content_based_merged_df

merged_df = get_content_based_merged_df()
pivot_table = pivot_table(merged_df, columns='User-ID', index='ISBN', values='Book-Rating').fillna(0)
knn = NearestNeighbors(metric = 'cosine', algorithm = 'brute')
knn.fit(pivot_table)

with open("../bookshelf/knn.pkl", "wb") as model_file, open("../bookshelf/pivot_table.pkl", "wb") as pivot_file:
    pickle.dump(knn, model_file)
    pickle.dump(pivot_table, pivot_file)
