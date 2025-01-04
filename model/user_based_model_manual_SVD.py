import pickle

import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

from model.preprocess_data import get_merged_df


def create_user_item_matrix(df, all_books):
    user_item_matrix = df.pivot(index='User-ID', columns='ISBN', values='Book-Rating')
    user_item_matrix = user_item_matrix.reindex(columns=all_books)

    return user_item_matrix


# Gradient Descent
def matrix_factorization(R, K, steps, alpha, beta):
    num_users, num_items = R.shape
    P = np.random.rand(num_users, K)  # Users matrix
    Q = np.random.rand(num_items, K)  # Books matrix

    Q = Q.T
    history = []

    for step in range(steps):
        for i in range(num_users):
            for j in range(num_items):
                if R[i, j] > 0:
                    error = R[i, j] - np.dot(P[i, :], Q[:, j])
                    for k in range(K):
                        P[i, k] += alpha * (2 * error * Q[k, j] - beta * P[i, k])
                        Q[k, j] += alpha * (2 * error * P[i, k] - beta * Q[k, j])

        R_pred = np.dot(P, Q)

        mask = R > 0
        mae = mean_absolute_error(R[mask], R_pred[mask])
        history.append(mae)
        print(f"Step {step + 1}, MAE: {mae:.4f}")

    return P, Q.T, history


def run_pipeline_SVD():
    df = get_merged_df()
    train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

    # Matrices needs to have the same shape for both train and test
    all_books = df['ISBN'].unique()
    train_matrix = create_user_item_matrix(train_df, all_books).values
    test_matrix = create_user_item_matrix(test_df, all_books).values

    steps = 100
    P, Q, train_mae_history = matrix_factorization(train_matrix, K=40, steps=steps, alpha=0.0002, beta=0.3)

    R_pred = np.dot(P, Q.T)
    mask = test_matrix > 0
    test_mae = mean_absolute_error(test_matrix[mask], R_pred[mask])
    print(f"\nMAE on test: {test_mae:.4f}")

    # Plot MAE evolution
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, steps + 1), train_mae_history, marker='o', label="Training MAE")
    plt.axhline(y=test_mae, color='r', linestyle='--', label="Test MAE")
    plt.title("MAE evolution during training and evaluation on test")
    plt.xlabel("Epochs")
    plt.ylabel("MAE")
    plt.legend()
    plt.grid()
    plt.show()

    return P, Q


P, Q = run_pipeline_SVD()

# Save the matrices
with open("../bookshelf/model_P.pkl", "wb") as model_P, open("../bookshelf/model_Q.pkl", "wb") as model_Q:
    pickle.dump(P, model_P)
    pickle.dump(Q, model_Q)
