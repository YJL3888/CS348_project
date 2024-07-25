import config
import os
import bcrypt
from flask import Flask, request
from flask_cors import CORS
import secrets
from flask_jwt_extended import create_access_token, current_user, JWTManager, jwt_required
import operator
from datetime import datetime
from db_util import create_connection, hash_password
import restaurants
import password_reset


app = Flask(__name__)
CORS(app, origins=os.environ['CORS_ORIGINS'])
app.config['JWT_SECRET_KEY'] = secrets.token_hex(64)
jwt = JWTManager(app)
app.register_blueprint(restaurants.bp)
app.register_blueprint(password_reset.bp)


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
                           (username, hash_password(password), email))
            connection.commit()
            return {'access_token': create_access_token(identity=cursor.lastrowid, additional_claims={
                'username': username, 'email': email
            })}


@app.post('/favorites')
@jwt_required()
def add_to_favorites():
    data = request.get_json()
    user_id = current_user['user_id']
    restaurant_id = data['restaurant_id']
    with create_connection() as connection:
        with connection.cursor(prepared=True) as cursor:
            cursor.execute('INSERT INTO Favorites(user_id, restaurant_id) VALUES (%s, %s)', (user_id, restaurant_id))
            connection.commit()
            return {'message': 'Restaurant added to favorites'}


@app.get('/favorites')
@jwt_required()
def get_favorites():
    user_id = current_user['user_id']
    with create_connection() as connection:
        with connection.cursor(prepared=True) as cursor:
            cursor.execute('SELECT * FROM Favorites WHERE user_id=%s', (user_id,))
            favs = cursor.fetchall()
            return favs


@app.post('/reviews')
@jwt_required()
def add_review():
    data = request.get_json()
    restaurant_id = data['restaurant_id']
    user_id = current_user['user_id']
    rating = data['rating']
    comments = data.get('comments', '')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    with create_connection() as connection:
        with connection.cursor(prepared=True) as cursor:
            cursor.execute('INSERT INTO Reviews(restaurant_id, user_id, rating, comments, timestamp) VALUES (%s, %s, %s, %s, %s)', (restaurant_id, user_id, rating, comments, timestamp))
            connection.commit()
            
            return {'message': 'Review added successfully!'}
        
        
@app.get('/reviews/<int:restaurant_id>')
def get_review(restaurant_id):
    with create_connection() as connection:
        with connection.cursor(prepared=True) as cursor:
            cursor.execute('SELECT * FROM Reviews WHERE restaurant_id=%s', (restaurant_id,))
            reviews = cursor.fetchall()
            return reviews
        
@app.get('/recommendations')
def get_recommendations():
    with create_connection() as connection:
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute('''
                SELECT restaurant_id, AVG(rating) as avg_rating
                FROM Reviews
                GROUP BY restaurant_id
                ORDER BY avg_rating DESC
                LIMIT 10
            ''')
            recs = cursor.fetchall()
            return recs

if __name__ == '__main__':
    app.run()
