import mysql.connector
import bcrypt
from flask import Flask, request, abort
from flask_cors import CORS
import config
import secrets
from flask_jwt_extended import create_access_token, current_user, JWTManager, jwt_required
import operator


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
            cursor.execute("SELECT * FROM Users WHERE email=%s", (request.form['email'],))
            user = cursor.fetchone()
            print('User', user)
            if user and bcrypt.checkpw(request.form['password'].encode('utf-8'), user['password'].encode('utf-8')):
                return {'access_token': create_access_token(identity=user['user_id'], additional_claims={
                    'username': user['username'],
                    'email': user['email']
                })}
            else:
                return {'error': 'Incorrect username or password.'}, 401


@app.get('/whoami')
@jwt_required()
def who():
    # intentionally ungolfy for demonstration
    return {
        'id': current_user['user_id'],
        'username': current_user['username'],
        'email': current_user['email']
    }


@app.post('/register')
def register():
    username, password, email = operator.itemgetter('username', 'password', 'email')(request.form)
    with create_connection() as connection:
        with connection.cursor(prepared=True) as cursor:
            cursor.execute('SELECT * FROM Users where username=%s', (username,))
            if cursor.fetchone():
                return {'error': 'Username already exists'}, 400
            cursor.execute('SELECT * FROM Users where email=%s', (email,))
            if cursor.fetchone():
                return {'error': 'Email already exists'}, 400
            cursor.execute('INSERT INTO Users(username, password, email) VALUES (%s, %s, %s)',
                           (username, bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()), email))
            connection.commit()
            return {'access_token': create_access_token(identity=cursor.lastrowid, additional_claims={
                'username': username, 'email': email
            })}


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
            return rows
        
@app.get('/restaurants')
def get_restaurants():
    """Endpoint to get restaurants from the database"""
    with create_connection() as conn:
        with conn.cursor() as cursor:
            query = "SELECT * FROM Restaurants"
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows


@app.get('/random_restaurants')
def get_random_restaurants():
    """Endpoint to get random restaurants from the database"""
    with create_connection() as conn:
        with conn.cursor() as cursor:
            query = "SELECT * FROM Restaurants ORDER BY RAND() LIMIT 10"
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows

@app.get('/restaurants/<int:restaurant_id>/menu')
def get_menu(restaurant_id):
    query = "SELECT item_name, price FROM Items WHERE restaurant_id = %s"
    
    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, (restaurant_id,))
            rows = cursor.fetchall()
            menu = [{'name': row[0], 'price': row[1]} for row in rows]
            return menu
        
@app.get('/search_restaurants')
def search_restaurants():
    search_query = request.args.get('query', '')
    search_fields = request.args.get('fields', '').split(',')
    
    if not search_query:
        return [], 200

    if not search_fields:
        return {'error': 'fields are required'}, 400
    
    query_parts = []
    params = []
    
    if 'name' in search_fields:
        query_parts.append("restaurant_name LIKE %s")
        params.append(f"%{search_query}%")
    if 'cuisine' in search_fields:
        query_parts.append("cuisine LIKE %s")
        params.append(f"%{search_query}%")

    query = "SELECT * FROM Restaurants WHERE " + " OR ".join(query_parts)
    
    print("Executing query:", query)
    print("With parameters:", params)
    
    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return rows

if __name__ == '__main__':
    # create_account(create_connection(), 'test', 'test123!', 'test@user.com')
    app.run()
