CREATE TABLE IF NOT EXISTS books (
    ISBN TEXT PRIMARY KEY,
    Book_Title TEXT,
    Book_Author TEXT,
    Year_Of_Publication INTEGER,
    Publisher TEXT,
    Image_URL TEXT
);

CREATE TABLE IF NOT EXISTS users (
    User_ID SERIAL PRIMARY KEY,
    Username TEXT,
    Password TEXT,
    Location TEXT,
    Age REAL
);

CREATE TABLE IF NOT EXISTS ratings (
    User_ID INTEGER REFERENCES users(User_ID) ON DELETE CASCADE,
    ISBN TEXT REFERENCES books(ISBN) ON DELETE CASCADE,
    Book_Rating INTEGER CHECK (Book_Rating BETWEEN 0 AND 10),
    PRIMARY KEY (User_ID, ISBN)
);


COPY books (ISBN, Book_Title, Book_Author, Year_Of_Publication, Publisher, Image_URL)
FROM '/docker-entrypoint-initdb.d/books.csv'
DELIMITER ',' CSV HEADER;

COPY users (User_ID, Location, Age)
FROM '/docker-entrypoint-initdb.d/users.csv'
DELIMITER ',' CSV HEADER;

COPY ratings (User_ID, ISBN, Book_Rating)
FROM '/docker-entrypoint-initdb.d/ratings.csv'
DELIMITER ',' CSV HEADER;
