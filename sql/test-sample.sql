SHOW DATABASES;
SHOW TABLES;
USE sample_data;

SELECT username, email FROM Users WHERE user_id = 1;
SELECT * FROM Items WHERE restaurant_id = 3;
SELECT * FROM Reviews WHERE restaurant_id = 2;
SELECT * FROM Favorites WHERE user_id = 1;
SELECT * FROM Restaurant WHERE cuisine = 'chinese'; 
SELECT * FROM Discount WHERE restaurant_id = 1;

SELECT username, email FROM Users WHERE user_id = 1;

SELECT * FROM Items WHERE restaurant_id = 3;

INSERT INTO Reviews (restaurant_id, user_id, rating, comments, timestamp)
VALUES (2, 3, 4, 'Tuna...', '2024-07-01 00:00:00');
SELECT * FROM Reviews WHERE restaurant_id = 2;

INSERT INTO Favorites (user_id, restaurant_id)
VALUES (4, 1);
SELECT * FROM Favorites WHERE user_id = 1;

SELECT * FROM Restaurant WHERE cuisine = 'chinese';

SELECT * FROM Discount WHERE restaurant_id = 1;
