import mysql.connector
import os
import bcrypt

def create_connection():
    """Create a database connection to the database"""
    return mysql.connector.connect(
        host='goosegoosego.clegmk4ois3q.us-east-1.rds.amazonaws.com',
        user='admin',
        password=os.getenv('DB_PASSWORD'),
        database='sample_data'
    )

def hash_password(password):
    """Hash a password for storing."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def create_account(conn, username, password, email):
    """Create a new user account"""
    hashed_password = hash_password(password)
    with conn.cursor() as cursor:
        query = "INSERT INTO Users (username, password, email) VALUES (%s, %s, %s)"
        cursor.execute(query, (username, hashed_password, email))
        conn.commit()
        print('Account created successfully.')

def add_to_favorites(conn, user_id, restaurant_id):
    """Add a restaurant to a user's favorites"""
    with conn.cursor() as cursor:
        query = "INSERT INTO Favorites (user_id, restaurant_id) VALUES (%s, %s)"
        cursor.execute(query, (user_id, restaurant_id))
        conn.commit()
        print('Restaurant added to favorites.')


def select_items(conn):
    """Query the database and print the results."""
    with conn.cursor() as cursor:
        query = "SELECT * FROM Items"
        cursor.execute(query)
        rows = cursor.fetchall()

        print('Printing items')
        for row in rows:
            print(row)


if __name__ == '__main__':
    with create_connection() as connection:
        select_items(connection)
