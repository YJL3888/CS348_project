import json
import traceback
import mysql.connector
from app import create_connection

# Load the JSON file
with open('../data_collection/restaurantData.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Open connection
conn = create_connection()
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

# Open a log file to write errors
with open('error_log.txt', 'w', encoding='utf-8') as error_log:
    for item in data:
        try:
            hours_range = convert_hours(item['hours'])

            restaurant_values = (item['name'], item['address'], item['category'], hours_range)
            cur.execute(insert_restaurant_query, restaurant_values)
            restaurant_id = cur.lastrowid  # Get the ID of the last inserted row
            for menu_item in item['menuItems']:
                try:
                    # Remove the dollar sign from the price and convert it to a float
                    price = float(menu_item['price'].replace('$', ''))
                    price /= 1.2
                    price += 0.01
                    price = round(price * 10) / 10
                    price -= 0.01
                    item_values = (menu_item['name'], restaurant_id, price)
                    cur.execute(insert_item_query, item_values)
                except mysql.connector.Error as err:
                    if err.errno == 1062:
                        error_log.write(f"Duplicate menu item {menu_item['name']} in restaurant {item['name']}: {str(err)}\n")
                    else:
                        raise
            print(f"Successfully processed restaurant {item['name']}")
        except Exception as e:
            # Write the item and the error to the log file
            error_log.write(f"Error processing item {item}: {str(e)}\n")
            error_log.write(traceback.format_exc() + "\n")

conn.commit()
cur.close()
conn.close()