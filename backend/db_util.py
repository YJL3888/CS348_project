import mysql.connector
import os
import bcrypt

_DB_PASSWORD = os.getenv('DB_PASSWORD')
_DB_NAME = os.getenv('ENV', 'prod') + '_data'


def create_connection():
    """Create a database connection to the database"""
    return mysql.connector.connect(
        host='goosegoosego.clegmk4ois3q.us-east-1.rds.amazonaws.com',
        user='admin',
        password=_DB_PASSWORD,
        database=_DB_NAME
    )


def hash_password(password: str):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
