import sqlite3; from sqlite3 import IntegrityError, ProgrammingError
import pandas as pd

conn = sqlite3.connect('bookdb.sqlite')
cur = conn.cursor()

def get_book(query) -> str:
    try:

        cur.execute(f"SELECT * FROM book WHERE title LIKE '%{query}%'")
        return cur.fetchall()

    except ProgrammingError:
        print(f"Book '{query}' does not exist.")
        return None


def get_author_id(query) -> str:
    try:
        cur.execute(f"SELECT author_fn, author_ln FROM author WHERE author_id =?", [query])
        return cur.fetchone()

    except ProgrammingError:
        print(f"Author ID:{query} does not exist.")
        return None

def is_user(query) -> str:
    try:
        cur.execute(f"SELECT COUNT(user_id) FROM user WHERE user_name =?", [query])
        return cur.fetchone()

    except ProgrammingError:
        print(f"Username {query} does not exist.")
        return None

def get_user(query):
    try:
        cur.execute(f"SELECT * FROM user WHERE user_name =?", [query])
        return cur.fetchone()

    except ProgrammingError:
        print(f"Username {query} does not exist.")
        return None

def get_data(table: str, conn: sqlite3.Connection = conn):

    return pd.read_sql(f'''SELECT * FROM {table}''', conn)
    
def insert_review(book_id: int, user_id: int, body: str, rating: float,):
    try:
        cur.execute(f"INSERT INTO review (book_id, user_id, body, rating) VALUES (?, ?, ?, ?)", [book_id, user_id, body, rating])
        conn.commit()

    except IntegrityError as e:
        print(e)

def insert_author(author_fn: str, author_ln: str):
    try:
        cur.execute(f"INSERT INTO author (author_fn, author_ln) VALUES (?, ?)", [author_fn, author_ln])
        conn.commit()

    except IntegrityError as e:
        print(e, msg)

def insert_book(
    author_id: int,
    title: str, 
    publish_date: str, 
    genre: str,
    book_cover: str = None
    ):
    
    try:
        cur.execute(f"INSERT INTO book (title, publish_date, genre, book_cover, author_id) VALUES (?, ?, ?, ?, ?)", [title, publish_date, genre, book_cover, author_id])
        conn.commit()

    except IntegrityError as e:
        print(e)