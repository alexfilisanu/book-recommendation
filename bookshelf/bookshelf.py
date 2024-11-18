import os

import psycopg2
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )
    return conn


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
            b.Year_Of_Publication,
            b.Publisher,
            b.Image_URL_L,
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
                "Year_Of_Publication": row[3],
                "Publisher": row[4],
                "Image_URL_L": row[5],
                "Average_Rating": round(row[6], 2),
            }
            for row in books
        ]

        conn.close()
        return jsonify({"books": books_list}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=3050, host='0.0.0.0')
