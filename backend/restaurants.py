from flask import Blueprint, request
from db_util import create_connection

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
