SHOW DATABASES;
SHOW TABLES;
USE sample_data;

SELECT username, email FROM Users WHERE user_id = 1;
SELECT * FROM Items WHERE restaurant_id = 3;
SELECT * FROM Reviews WHERE restaurant_id = 2;
SELECT * FROM Favorites WHERE user_id = 1;
SELECT * FROM Restaurant WHERE cuisine = 'chinese'; 
SELECT * FROM Discount WHERE restaurant_id = 1;
