import sqlite3

def initiate_db():
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Products(
    id INT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INT NOT NULL
    )
    """)
    # cursor.execute("DROP TABLE Users")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Users(
    id AUTO_INCREMENT INT PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INT NOT NULL,
    balance INT NOT NULL
    )
    """)
    connection.commit()
    connection.close()

def add_user(username, email, age):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)",
                   (username, email, age, 1000))
    connection.commit()
    connection.close()

def is_included(username):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute("SELECT username FROM Users")
    users = cursor.fetchall()
    usernames_list = [user[0] for user in users]
    connection.close()
    return username in usernames_list

def get_all_products():
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Products")
    products = cursor.fetchall()
    connection.close()
    return products

def main():
    initiate_db()
if __name__ == "__main__":
    main()