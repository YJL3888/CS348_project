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
        
@bp.post('/toggle_favorites')
def toggle_favorites():
    data = request.get_json()
    user_id = data.get('user_id')
    restaurant_id = data.get('restaurant_id')

    if not user_id or not restaurant_id:
        return {'error': 'Both user_id and restaurant_id are required'}, 400

    try:
        with create_connection() as conn:
            with conn.cursor() as cursor:
                # Check if the entry already exists
                check_query = "SELECT EXISTS(SELECT 1 FROM Favorites WHERE user_id=%s AND restaurant_id=%s)"
                cursor.execute(check_query, (user_id, restaurant_id))
                exists = cursor.fetchone()[0]

                if exists:
                    # If exists, remove it
                    delete_query = "DELETE FROM Favorites WHERE user_id=%s AND restaurant_id=%s"
                    cursor.execute(delete_query, (user_id, restaurant_id))
                else:
                    # If not exists, add it
                    insert_query = "INSERT INTO Favorites (user_id, restaurant_id) VALUES (%s, %s)"
                    cursor.execute(insert_query, (user_id, restaurant_id))

                conn.commit()
                action = "removed from" if exists else "added to"
                return {'message': f'Restaurant {action} favorites successfully'}, 200
    except Exception as e:
        print(f"Error toggling favorite: {e}")
        return {'error': 'Failed to toggle favorite'}, 500
    
@bp.get('/favorites')
def get_favorites():
    user_id = request.args.get('user_id', default=None, type=int)
    if not user_id:
        return jsonify({'error': 'Missing user_id'}), 400

    query = "SELECT restaurant_id FROM Favorites WHERE user_id = %s"

    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, (user_id,))
            rows = cursor.fetchall()
            favorite_restaurant_ids = [row[0] for row in rows]

    return favorite_restaurant_ids, 200