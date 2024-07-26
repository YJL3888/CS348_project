from flask import Blueprint, request, abort
from db_util import create_connection
from flask_jwt_extended import jwt_required, current_user
from datetime import datetime

bp = Blueprint('restaurants', __name__)


@bp.get('/restaurants')
def get_restaurants():
    """Endpoint to get restaurants from the database"""
    with create_connection() as conn:
        with conn.cursor() as cursor:
            query = "SELECT * FROM Restaurants"
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows


@bp.get('/random_restaurants')
def get_random_restaurants():
    """Endpoint to get random restaurants from the database"""
    with create_connection() as conn:
        with conn.cursor() as cursor:
            query = "SELECT * FROM Restaurants ORDER BY RAND() LIMIT 10"
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows


@bp.get('/restaurants/<int:restaurant_id>/menu')
def get_menu(restaurant_id):
    query = "SELECT item_name, price FROM Items WHERE restaurant_id = %s"

    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, (restaurant_id,))
            rows = cursor.fetchall()
            menu = [{'name': row[0], 'price': row[1]} for row in rows]
            return menu


@bp.get('/restaurants/<int:restaurant_id>')
def get_restaurant(restaurant_id):
    with create_connection() as conn:
        with conn.cursor(prepared=True, dictionary=True) as cursor:
            cursor.execute("SELECT * FROM Restaurants WHERE restaurant_id=%s", (restaurant_id,))
            if not (restaurant := cursor.fetchone()):
                abort(404)
            cursor.execute("SELECT * FROM Items WHERE restaurant_id=%s", (restaurant_id,))
            restaurant['menu'] = cursor.fetchall()
            cursor.execute("SELECT * FROM Reviews NATURAL JOIN Users WHERE restaurant_id=%s ORDER BY `timestamp` DESC", (restaurant_id,))
            restaurant['reviews'] = cursor.fetchall()
            cursor.execute('SELECT * FROM Comments NATURAL JOIN Users WHERE restaurant_id=%s AND deleted=0 ORDER BY posted_time', (restaurant_id,))
            restaurant['comments'] = cursor.fetchall()
            cursor.execute('SELECT * FROM Discount WHERE restaurant_id=%s', (restaurant_id,))
            restaurant['discounts'] = cursor.fetchall()
            return restaurant


@bp.post('/restaurants/review')
@jwt_required()
def add_review():
    with create_connection() as connection:
        with connection.cursor(prepared=True, dictionary=True) as cursor:
            cursor.execute('''
            INSERT INTO Reviews(restaurant_id, user_id, rating, comments, timestamp) VALUES (%s, %s, %s, %s, %s)
            ''', (request.form['restaurant_id'], current_user['user_id'], request.form['rating'], 
                  request.form('review'), datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            connection.commit()
            cursor.execute('SELECT * FROM Reviews NATURAL JOIN Users WHERE review_id=%s', (cursor.lastrowid,))
            return cursor.fetchone()


@bp.post('/restaurants/comment')
@jwt_required()
def comment_on_restaurant():
    with create_connection() as connection:
        with connection.cursor(prepared=True, dictionary=True) as cursor:
            cursor.execute('''
            INSERT INTO Comments(content, restaurant_id, user_id, parent_comment_id) VALUES(%s, %s, %s, %s)
            ''', (request.form['content'], request.form['restaurant_id'],
                  current_user['user_id'], request.form.get('parent_comment_id')))
            connection.commit()
            cursor.execute('SELECT * FROM Comments NATURAL JOIN Users WHERE comment_id=%s', (cursor.lastrowid,))
            return cursor.fetchone()


@bp.post('/restaurants/comment/delete')
@jwt_required()
def delete_comment():
    print('delete', request.form)
    with create_connection() as connection:
        with connection.cursor(prepared=True, dictionary=True) as cursor:
            cursor.execute('UPDATE Comments SET deleted=1 WHERE comment_id=%s AND user_id=%s',
                           (request.form['comment_id'], current_user['user_id']))
            if cursor.rowcount != 1:
                abort(403)
            connection.commit()
            return {}


@bp.get('/search_restaurants')
def search_restaurants():
    search_query = request.args.get('query', '')
    search_fields = request.args.get('fields', '').split(',')

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

    query = """
    SELECT 
        r.*,
        CASE WHEN MAX(d.discount) IS NOT NULL THEN true ELSE false END as discount,
        COUNT(rv.review_id) as review_count,
        AVG(rv.rating) as average_rating
    FROM 
        Restaurants r
    LEFT JOIN 
        Discount d ON r.restaurant_id = d.restaurant_id
    LEFT JOIN 
        Reviews rv ON r.restaurant_id = rv.restaurant_id
    WHERE 
        """ + " OR ".join(query_parts) + """
    GROUP BY 
        r.restaurant_id
    """

    print("Executing query:", query)
    print("With parameters:", params)

    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return rows


@bp.post('/favorites/toggle')
@jwt_required()
def toggle_favorites():
    restaurant_id = request.json['restaurant_id']

    with create_connection() as conn:
        with conn.cursor() as cursor:
            # Check if the entry already exists
            check_query = "SELECT EXISTS(SELECT 1 FROM Favorites WHERE user_id=%s AND restaurant_id=%s)"
            cursor.execute(check_query, (current_user['user_id'], restaurant_id))
            exists = cursor.fetchone()[0]

            if exists:
                # If exists, remove it
                delete_query = "DELETE FROM Favorites WHERE user_id=%s AND restaurant_id=%s"
                cursor.execute(delete_query, (current_user['user_id'], restaurant_id))
            else:
                # If not exists, add it
                insert_query = "INSERT INTO Favorites (user_id, restaurant_id) VALUES (%s, %s)"
                cursor.execute(insert_query, (current_user['user_id'], restaurant_id))

            conn.commit()
            action = "removed from" if exists else "added to"
            return {'message': f'Restaurant {action} favorites successfully'}, 200


@bp.post('/favorites')
@jwt_required()
def get_favorites():
    query = "SELECT restaurant_id FROM Favorites WHERE user_id = %s"

    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, (current_user['user_id'],))
            rows = cursor.fetchall()
            favorite_restaurant_ids = [row[0] for row in rows]

    return favorite_restaurant_ids


@bp.get('/discounts/<int:restaurant_id>')
def get_discounts_for_restaurant(restaurant_id):
    with create_connection() as connection:
        with connection.cursor(prepared=True, dictionary=True) as cursor:
            cursor.execute('SELECT * FROM Discount WHERE restaurant_id=%s', (restaurant_id,))
            discounts = cursor.fetchall()
            return discounts


@bp.get('/discounts')
def get_discounts_for_day():
    weekday = request.args.get('weekday', '')
    if not weekday:
        return {'error': 'Weekday is required!'}
    
    with create_connection() as connection:
        with connection.cursor(prepared=True) as cursor:
            cursor.execute('SELECT * FROM Discount WHERE weekday=%s', (weekday))
            discounts = cursor.fetchall()
            return discounts
