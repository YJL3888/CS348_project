import json
from app import create_connection

# Load the JSON file
with open('../data_collection/restaurants.json') as f:
    data = json.load(f)

# Open a connection to the AWS RDS database
conn = create_connection()

# Create a cursor object
cur = conn.cursor()

# SQL query to insert data into Restaurants table
insert_restaurant_query = """
INSERT INTO Restaurants (restaurant_name, address, cuisine, hours_range) 
VALUES (%s, %s, %s, %s)
"""

# SQL query to insert data into Items table
insert_item_query = """
INSERT INTO Items (item_name, restaurant_id, Price) 
VALUES (%s, %s, %s)
"""

# Helper function to convert hours to the desired format
def convert_hours(hours):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    abbreviations = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
    new_hours = {}
    for day, abbreviation in zip(days, abbreviations):
        if day in hours:
            start, end = hours[day].split(' - ')
            start = start.replace(':','').replace(' a.m.', '').replace(' p.m.', '')
            end = end.replace(':','').replace(' a.m.', '').replace(' p.m.', '')
            new_hours[abbreviation] = f"{start}-{end}"
    return json.dumps(new_hours)

# Iterate over the JSON data and insert each record into the database
for item in data:
    # Convert hours to the desired format
    hours_range = convert_hours(item['hours'])

    # Insert restaurant data
    restaurant_values = (item['name'], item['address'], item['category'], hours_range)
    cur.execute(insert_restaurant_query, restaurant_values)
    restaurant_id = cur.lastrowid  # Get the ID of the last inserted row

    # Insert menu items data
    for menu_item in item['menuItems']:
        # Remove the dollar sign from the price and convert it to a float
        price = float(menu_item['price'].replace('$', ''))
        item_values = (menu_item['name'], restaurant_id, price)
        cur.execute(insert_item_query, item_values)

# Commit the transaction
conn.commit()

# Close the cursor and connection
cur.close()
conn.close()