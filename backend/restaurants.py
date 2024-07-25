from flask import Blueprint, request
from db_util import create_connection
from flask_jwt_extended import jwt_required, current_user

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


@bp.get('/search_restaurants')
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


@bp.get('/favorites')
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
        with connection.cursor(prepared=True) as cursor:
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
