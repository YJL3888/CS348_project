-- Replace with prod_data for production database
CREATE DATABASE sample_data;
USE sample_data;

CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password CHAR(64) NOT NULL,
    email VARCHAR(100) NOT NULL
);

CREATE TABLE Restaurant (
    restaurant_id AUTO_INCREMENT INT PRIMARY KEY,
    restaurant_name VARCHAR(100),
    description TEXT,
    address VARCHAR(255),
    phone_number VARCHAR(15),
    website VARCHAR(255),
    cuisine VARCHAR(50),
    price_range INT,
    hours_range VARCHAR(400)
);

CREATE TABLE Items (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    item_name VARCHAR(255),
    restaurant_id INT NOT NULL,
    Price FLOAT,
    FOREIGN KEY (restaurant_id) REFERENCES Restaurant(restaurant_id) ON DELETE CASCADE,
    UNIQUE (item_name, restaurant_id)
);

CREATE TABLE Discount (
    discount_id INT AUTO_INCREMENT PRIMARY KEY,
    restaurant_id INT NOT NULL,
    item_id INT,
    discount FLOAT,
    discount_type CHAR(1) NOT NULL,
    weekday CHAR(3),
    FOREIGN KEY (restaurant_id) REFERENCES Restaurant(restaurant_id) ON DELETE CASCADE,
    FOREIGN KEY (item_id) REFERENCES Items(item_id) ON DELETE CASCADE
);

CREATE TABLE Reviews (
    review_id INT AUTO_INCREMENT PRIMARY KEY,
    restaurant_id INT NOT NULL,
    user_id INT NOT NULL,
    rating INT NOT NULL,
    comments TEXT,
    timestamp TIMESTAMP,
    UNIQUE (restaurant_id, user_id),
    FOREIGN KEY (restaurant_id) REFERENCES Restaurant(restaurant_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

--this is a bonus feature and is not implemented yet for Milestone 1
CREATE TABLE ReviewVotes (
    review_id INT,
    upvotes INT,
    downvotes INT,
    FOREIGN KEY (review_id) REFERENCES Reviews(review_id)
);

CREATE TABLE Favorites (
    user_id INT,
    restaurant_id INT,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (restaurant_id) REFERENCES Restaurant(restaurant_id)
);
