import os
import pickle
import psycopg2
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# with open('knn.pkl', 'rb') as model_file, open('pivot_table.pkl', 'rb') as pivot_file:
#     knn = pickle.load(model_file)
#     pivot_table = pickle.load(pivot_file)
with open('blended_similarity.pkl', 'rb') as item_to_item_df, open('user_based_df.pkl', 'rb') as user_based_df:
    blended_similarity_df = pickle.load(item_to_item_df)
    predicted_ratings_df = pickle.load(user_based_df)


def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )


@app.route('/total-books', methods=['GET'])
def get_total_books():
    try:
        search_query = request.args.get('q', '')
        conn = get_db_connection()
        cursor = conn.cursor()

        query = f"""
        SELECT 
            COUNT(*) 
        FROM 
            books b
        WHERE
            b.Book_Title ILIKE %s
            OR b.Book_Author ILIKE %s
            OR b.ISBN ILIKE %s;
        """
        cursor.execute(query, (
            f"%{search_query}%",
            f"%{search_query}%",
            f"{search_query}"
        ))
        total_books = cursor.fetchone()[0]

        conn.close()
        return jsonify({"totalBooks": total_books}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/books', methods=['GET'])
def get_books():
    try:
        search_query = request.args.get('q', '')
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        offset = (page - 1) * limit

        conn = get_db_connection()
        cursor = conn.cursor()

        query = f"""
        SELECT 
            b.ISBN,
            b.Book_Title,
            b.Book_Author,
            b.Image_URL,
            COALESCE(AVG(r.Book_Rating), 0) AS Average_Rating
        FROM 
            books b
        LEFT JOIN 
            ratings r ON b.ISBN = r.ISBN
        WHERE
            b.Book_Title ILIKE %s
            OR b.Book_Author ILIKE %s
            OR b.ISBN ILIKE %s
        GROUP BY 
            b.ISBN
        ORDER BY 
            Average_Rating DESC
        LIMIT %s OFFSET %s;
        """
        cursor.execute(query, (
            f"%{search_query}%",
            f"%{search_query}%",
            f"{search_query}",
            limit,
            offset
        ))
        books = cursor.fetchall()

        books_list = [
            {
                "ISBN": row[0],
                "Book_Title": row[1],
                "Book_Author": row[2],
                "Image_URL": row[3],
                "Average_Rating": round(row[4], 2),
            }
            for row in books
        ]

        conn.close()
        return jsonify({"books": books_list}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/book/<isbn>/', methods=['GET'])
def get_book(isbn):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = f"""
        SELECT
            b.ISBN, 
            b.Book_Title,
            b.Book_Author,
            b.Year_Of_Publication,
            b.Publisher,
            b.Image_URL,
            COALESCE(AVG(r.Book_Rating), 0) AS Average_Rating
        FROM 
            books b
        LEFT JOIN 
            ratings r ON b.ISBN = r.ISBN
        WHERE
            b.ISBN = %s
        GROUP BY 
            b.ISBN;
        """
        cursor.execute(query, (isbn,))
        book = cursor.fetchone()

        book_dict = {
            "ISBN": book[0],
            "Book_Title": book[1],
            "Book_Author": book[2],
            "Year_Of_Publication": book[3],
            "Publisher": book[4],
            "Image_URL": book[5],
            "Average_Rating": round(book[6], 2),
        }

        conn.close()
        return jsonify({"book": book_dict}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/book/recommendations/<isbn>', methods=['GET'])
def get_book_recommendations(isbn):
    try:
        if isbn not in blended_similarity_df.index:
            return jsonify({'error': 'ISBN not found'}), 404

        # Get similar books from the blended similarity matrix
        similar_books = blended_similarity_df[isbn].sort_values(ascending=False)[1:6]
        recommended_isbns = similar_books.index.tolist()

        conn = get_db_connection()
        cursor = conn.cursor()

        query = f"""
        SELECT
            b.ISBN, 
            b.Book_Title,
            b.Book_Author,
            b.Year_Of_Publication,
            b.Publisher,
            b.Image_URL,
            COALESCE(AVG(r.Book_Rating), 0) AS Average_Rating
        FROM 
            books b
        LEFT JOIN 
            ratings r ON b.ISBN = r.ISBN
        WHERE
            b.ISBN = %s
        GROUP BY 
            b.ISBN;
        """

        recommendations = []
        for rec_isbn in recommended_isbns:
            cursor.execute(query, (rec_isbn,))
            book = cursor.fetchone()
            if book:
                recommendations.append({
                    "ISBN": book[0],
                    "Book_Title": book[1],
                    "Book_Author": book[2],
                    "Year_Of_Publication": book[3],
                    "Publisher": book[4],
                    "Image_URL": book[5],
                    "Average_Rating": round(book[6], 2),
                })

        conn.close()
        return jsonify({"recommendations": recommendations}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/user/recommendations/<user_id>', methods=['GET'])
def get_user_recommendations(user_id):
    try:
        if int(user_id) not in predicted_ratings_df.index:
            # Fallback for new users: Recommend popular books
            conn = get_db_connection()
            cursor = conn.cursor()

            query = f"""
            SELECT
                b.ISBN,
                b.Book_Title,
                b.Book_Author,
                b.Year_Of_Publication,
                b.Publisher,
                b.Image_URL,
                COALESCE(AVG(r.Book_Rating), 0) AS Average_Rating
            FROM 
                books b
            LEFT JOIN 
                ratings r ON b.ISBN = r.ISBN
            GROUP BY 
                b.ISBN
            ORDER BY 
                Average_Rating DESC
            LIMIT 10;
            """

            cursor.execute(query)
            books = cursor.fetchall()

            recommendations = []
            for book in books:
                recommendations.append({
                    "ISBN": book[0],
                    "Book_Title": book[1],
                    "Book_Author": book[2],
                    "Year_Of_Publication": book[3],
                    "Publisher": book[4],
                    "Image_URL": book[5],
                    "Average_Rating": round(book[6], 2),
                })

            conn.close()
            return jsonify({"recommendations": recommendations}), 200

        # User exists in predicted_ratings_df
        user_ratings = predicted_ratings_df.loc[int(user_id)].sort_values(ascending=False)
        recommended_isbns = user_ratings.head(10).index.tolist()

        conn = get_db_connection()
        cursor = conn.cursor()

        query = f"""
        SELECT
            b.ISBN, 
            b.Book_Title,
            b.Book_Author,
            b.Year_Of_Publication,
            b.Publisher,
            b.Image_URL,
            COALESCE(AVG(r.Book_Rating), 0) AS Average_Rating
        FROM 
            books b
        LEFT JOIN 
            ratings r ON b.ISBN = r.ISBN
        WHERE
            b.ISBN = %s
        GROUP BY 
            b.ISBN;
        """

        recommendations = []
        for rec_isbn in recommended_isbns:
            cursor.execute(query, (rec_isbn,))
            book = cursor.fetchone()
            if book:
                recommendations.append({
                    "ISBN": book[0],
                    "Book_Title": book[1],
                    "Book_Author": book[2],
                    "Year_Of_Publication": book[3],
                    "Publisher": book[4],
                    "Image_URL": book[5],
                    "Average_Rating": round(book[6], 2),
                })

        conn.close()
        return jsonify({"recommendations": recommendations}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/total-reviews', methods=['GET'])
def get_my_total_reviews():
    user_id = int(request.args.get('userId'))

    if not user_id:
        return jsonify({'error': 'Missing required data'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = f"""
        SELECT
            COUNT(*)
        FROM
            ratings
        WHERE
            User_ID = %s;
        """
        cursor.execute(query, (user_id,))
        total_reviews = cursor.fetchone()[0]

        conn.close()
        return jsonify({'totalReviews': total_reviews}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/reviews', methods=['GET'])
def get_my_reviews():
    user_id = int(request.args.get('userId'))
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    offset = (page - 1) * limit

    if not user_id:
        return jsonify({'error': 'Missing required data'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = f"""
        SELECT
            b.ISBN,
            b.Book_Title,
            b.Book_Author,
            b.Image_URL,
            r.Book_Rating
        FROM
            ratings r
        JOIN
            books b ON r.ISBN = b.ISBN
        WHERE
            r.User_ID = %s
        ORDER BY
            r.Book_Rating DESC
        LIMIT %s OFFSET %s;
        """
        cursor.execute(query, (user_id, limit, offset))
        reviews = cursor.fetchall()

        reviews_list = [
            {
                "ISBN": row[0],
                "Book_Title": row[1],
                "Book_Author": row[2],
                "Image_URL": row[3],
                "Average_Rating": row[4],
            }
            for row in reviews
        ]

        conn.close()
        return jsonify({'reviews': reviews_list}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/book/review/status', methods=['GET'])
def get_review_status():
    user_id = int(request.args.get('userId'))
    isbn = request.args.get('isbn')

    if not user_id or not isbn:
        return jsonify({'error': 'Missing required data'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = f"""
        SELECT
            Book_Rating
        FROM
            ratings
        WHERE
            User_ID = %s
            AND ISBN = %s;
        """
        cursor.execute(query, (user_id, isbn))
        book_rating = cursor.fetchone()

        conn.close()
        return jsonify({'bookRating': book_rating}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/book/review', methods=['POST'])
def add_book_review():
    data = request.json
    if not data:
        return jsonify({'No data provided'}), 400

    user_id = int(data.get('userId'))
    isbn = data.get('isbn')
    rating = int(data.get('rating'))

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = f"""
        INSERT INTO 
            ratings (User_ID, ISBN, Book_Rating)
        VALUES 
            (%s, %s, %s);
        """
        cursor.execute(query, (user_id, isbn, rating))
        conn.commit()

        conn.close()
        return jsonify({"message": "Review added successfully"}), 200

    except Exception as e:
        return jsonify({str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=3050, host='0.0.0.0')
