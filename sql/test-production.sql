
-- Use sample_data database
USE prod_data;

-- Show tables
SHOW TABLES;

-- Create a new user
INSERT IGNORE INTO Users (username, password, email) VALUES ('howard', '006cc76799242f7d99f74d80fb30bbd0ddcaa3bba5798caca638071482774527', 'hlou@uwaterloo.ca');

-- Select username and email from Users where user_id is 1
SELECT username, email FROM Users WHERE user_id = 1 LIMIT 10;

-- Select all items from Items where restaurant_id is 34
SELECT * FROM Items WHERE restaurant_id = 34 LIMIT 10;

-- Insert a review into Reviews
INSERT IGNORE INTO Reviews (restaurant_id, user_id, rating, comments, timestamp)
VALUES (33, 1, 4, 'The Margherita pizza was delicious, with a perfect balance of cheese and tomato sauce.', '2024-06-06 12:30:00');

-- Select all reviews from Reviews where restaurant_id is 33
SELECT * FROM Reviews WHERE restaurant_id = 33 LIMIT 10;

-- Insert a favorite into Favorites
INSERT IGNORE INTO Favorites (user_id, restaurant_id)
VALUES (1, 45);

-- Select all favorites from Favorites where user_id is 1
SELECT * FROM Favorites WHERE user_id = 1 LIMIT 10;

-- Select all restaurants where cuisine is 'Pizza'
SELECT * FROM Restaurants WHERE cuisine = 'Pizza' LIMIT 10;

-- Select discounts on Wednesday
SELECT * FROM Discount WHERE weekday = 'wed' LIMIT 10;
