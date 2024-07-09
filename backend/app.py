import mysql.connector
import bcrypt
from flask import Flask, request, abort
from flask_cors import CORS
import config
import secrets
from flask_jwt_extended import create_access_token, current_user, JWTManager, jwt_required


app = Flask(__name__)
CORS(app, origins='http://localhost:5173')
app.config['JWT_SECRET_KEY'] = secrets.token_hex(64)
jwt = JWTManager(app)

DB_PASSWORD = config.DB_PASSWORD
DB_NAME = config.DB_NAME


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user['user_id']


@jwt.user_lookup_loader
def user_lookup(_jwt_header, jwt_data):
    with create_connection() as connection:
        with connection.cursor(prepared=True, dictionary=True) as cursor:
            cursor.execute('SELECT * FROM Users WHERE user_id=%s', (jwt_data["sub"],))
            return cursor.fetchone()


@app.post('/login')
def login():
    with create_connection() as connection:
        with connection.cursor(prepared=True, dictionary=True) as cursor:
            print(request.form['username'])
            cursor.execute("SELECT * FROM Users WHERE username=%s", (request.form['username'],))
            user = cursor.fetchone()
            print('User', user)
            if user and bcrypt.checkpw(request.form['password'].encode('utf-8'), user['password'].encode('utf-8')):
                return {'access_token': create_access_token(identity=user)}
            else:
                abort(401)


@app.get('/whoami')
@jwt_required()
def who():
    # intentionally ungolfy for demonstration
    return {
        'id': current_user['user_id'],
        'username': current_user['username'],
        'email': current_user['email']
    }


def create_connection():
    """Create a database connection to the database"""
    return mysql.connector.connect(
        host='goosegoosego.clegmk4ois3q.us-east-1.rds.amazonaws.com',
        user='admin',
        password=DB_PASSWORD,
        database=DB_NAME
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

@app.get('/items')
def get_items():
    """Endpoint to get items from the database"""
    with create_connection() as conn:
        with conn.cursor() as cursor:
            query = "SELECT * FROM Items"
            cursor.execute(query)
            rows = cursor.fetchall()
            return (rows)
        
@app.get('/restaurants')
def get_restaurants():
    """Endpoint to get restaurants from the database"""
    with create_connection() as conn:
        with conn.cursor() as cursor:
            query = "SELECT * FROM Restaurants"
            cursor.execute(query)
            rows = cursor.fetchall()
            return (rows)


if __name__ == '__main__':
    # create_account(create_connection(), 'test', 'test123!', 'test@user.com')
    app.run()
