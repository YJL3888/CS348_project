
-- Use sample_data database
USE prod_data;

-- Show tables
SHOW TABLES;

-- Select username and email from Users where user_id is 1
SELECT username, email FROM Users WHERE user_id = 1 LIMIT 10;

-- Select all items from Items where restaurant_id is 3
SELECT * FROM Items WHERE restaurant_id = 3 LIMIT 10;

-- Select all reviews from Reviews where restaurant_id is 2
SELECT * FROM Reviews WHERE restaurant_id = 2 LIMIT 10;

-- Select all favorites from Favorites where user_id is 1
SELECT * FROM Favorites WHERE user_id = 1 LIMIT 10;

-- Select all restaurants where cuisine is 'chinese'
SELECT * FROM Restaurant WHERE cuisine = 'chinese' LIMIT 10;

-- Select all discounts where restaurant_id is 1
SELECT * FROM Discount WHERE restaurant_id = 1 LIMIT 10;

-- Insert a review into Reviews
INSERT INTO Reviews (restaurant_id, user_id, rating, comments, timestamp)
VALUES (2, 3, 4, 'Tuna...', '2024-07-01 00:00:00');

-- Select all reviews from Reviews where restaurant_id is 2
SELECT * FROM Reviews WHERE restaurant_id = 2 LIMIT 10;

-- Insert a favorite into Favorites
INSERT INTO Favorites (user_id, restaurant_id)
VALUES (4, 1);

-- Select all favorites from Favorites where user_id is 1
SELECT * FROM Favorites WHERE user_id = 1 LIMIT 10;

-- Select all restaurants where cuisine is 'chinese'
SELECT * FROM Restaurant WHERE cuisine = 'chinese' LIMIT 10;

-- Select all discounts where restaurant_id is 1
SELECT * FROM Discount WHERE restaurant_id = 1 LIMIT 10;
