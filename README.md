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
4. Test connection to make sure everything is working and click OK.
5. You are now connected to the RDS database!

### Create Sample Database
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

### Scrape the Production Database
First, run data_collection/getRestaurants.js with Node. Make sure appropriate packages are installed (puppeteer)

This should generate a file restaurants.json, and a file errors.json for various error logging.

Next, run data_collection/processRestaurants.js with Node. This should generate a file restaurantData.json. You may have to bookend the file with [] to format it properly for the upload phase.

Finally, change the ENV field in backend's .env file to "prod" and run backend/uploadData.py. This should upload all the scraped data to the database appropriately.


## App Setup
Follow these steps to set up and run the application.

### Clone the Repository

First, clone the repository to your local machine:

```sh
git clone https://github.com/YJL3888/GooseGooseGo_CS348.git
cd GooseGooseGo_CS348
```

### Run the Application

Before running the application, the environment variables need to be setup. To do so, create a `.env` file in the root directory.
It should include `ENV` for choosing the sample or production database and `DB_PASSWORD` with the password to access the database.
Here is a sample `.env` file:

```
DB_PASSWORD=$DATABASE_PASSWORD
ENV="prod"
```
Replace `$DATABASE_PASSWORD` with your actual database password.

Run the backend python application:

```sh
cd backend
pip install -r requirements.txt
python app.py
```

Then run the frontend with
```sh
cd frontend
npm install
npm run dev
```

---

### Notes

- Ensure you have Python and `pip` installed on your machine.
- Make sure your database is set up and accessible from your development environment.
