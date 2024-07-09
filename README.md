# Goose Goose Go - CS348 Project

## Description
This project aims to develop a web application for tracking menus, ingredients, and prices of various food places in Waterloo.

## Database Setup
For our project, we have decided to use AWS RDS running MySQL in the us-east-1 (N.Virginia) Region. 

### Connection
1. To connect to the database, first download MySQL Workbench ```https://www.mysql.com/products/workbench/```
2. Create a new connection by clicking the '+' sign beside "MySQL Connections"
3. **Enter Connection Details:**
   - **Hostname:** Enter the RDS endpoint from AWS. You can find this in the AWS Management Console under the RDS instance details. It usually looks like `your-db-instance.c123456789012.us-west-2.rds.amazonaws.com`.
   - **Port:** Enter the port number your database listens on. The default port for MySQL is `3306`.
   - **Username/Password:** Enter the database username/password provided by your AWS RDS setup.
4. Test connection to make sure everything is working and click OK
5. You are now connected to the RDS database!

### Create Sample Database
Here are the queries necessary to create a sample database

Create a database and use it for upcoming queries
```sql
CREATE DATABASE sample_db;
USE sample_db;
```
Create table for `food_items`
```sql
CREATE TABLE food_items(
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    description TEXT
)
```
Load sample data into the database
```sql
INSERT INTO food_items (name, price, description) VALUES ('RiceNoodle', 0.00, 'rice noodle refils are free at Yunshang');
INSERT INTO food_items (name, price, description) VALUES ('Foodie Sushi', 16.00, 'foodie fruity has a varity of selection including sushis');
```

The database has been loaded with sample data! You can check it out with
```sql
SELECT * FROM food_items
```

## App Setup
Follow these steps to set up and run the application.

### Clone the Repository

First, clone the repository to your local machine:

```sh
git clone https://github.com/YJL3888/GooseGooseGo_CS348.git
cd GooseGooseGo_CS348
```

### Install Dependencies

Use `pip` to install the required dependencies from the `requirements.txt` file:

```sh
pip install -r requirements.txt
```

### Run the Application

Finally, run the application with your database password:

```sh
DB_PASSWORD=YOUR_PASSWORD python app/app.py
```

Replace `YOUR_PASSWORD` with your actual database password.

---

### Notes

- Ensure you have Python and `pip` installed on your machine.
- Make sure your database is set up and accessible from your development environment.
