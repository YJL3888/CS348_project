Insert Into Users (username, password, email) Values ('jasonliu', '904f0415fd9a0e6c94c00564c56193db7477a478f716a14c4963f5f06eeb102a', 'yj7liu@uwaterloo.ca');
Insert Into Users (username, password, email) Values ('jackli', '0070b5141d24f9b423f5a4d6e446e6b6255ba025b2a9bfa3c3e2e409e3ec922c', 'j279li@uwaterloo.ca');
Insert Into Users (username, password, email) Values ('RedcXca', 'e52817ddc8ef3a63b520212eceded3fbddb82333156600a79b2106a8ea4ea63f', 'm22lu@uwaterloo.ca');
Insert Into Users (username, password, email) Values ('jasoncheng', '007ab256a8197aa439026d15367c7ce6533cbcbd883de3c9143b868d751a1348', 'j25cheng@uwaterloo.ca');
Insert Into Users (username, password, email) Values ('howard', '006cc76799242f7d99f74d80fb30bbd0ddcaa3bba5798caca638071482774527', 'hlou@uwaterloo.ca');

INSERT INTO Restaurant (restaurant_name, description, address, phone_number, website, cuisine, price_range, hours_range) VALUES 
('Gol’s Lanzhou Noodles', 'noodles from lan zhou', '150 University Ave W Unit 6B, Waterloo, ON N2L 3E4', '(519) 208-3923', 'lanzhou.ca', 'chinese', 2, '{ "tue": "1100-2100", "wed": "1100-2100", "thu": "1100-2100", "fri": "1100-2100", "sat": "1100-2100", "sun": "1100-2100" }'),
('Foodie Fruitie', 'Asian fusion restaurant', '203 Lester St #7, Waterloo, ON N2L 0B5', '(519) 880-8688', NULL, 'asian fusion', 1, '{ "mon": "1500-2300", "tue": "1100-2300", "wed": "1100-2300", "thu": "1100-2300", "fri": "1100-2300", "sat": "1100-2300", "sun": "1100-2300" }'),
('Burger King', 'Fast food burgers chain', '150 University Ave W Unit 1a, Waterloo, ON N2L 3E4', '(519) 884-6072', 'https://www.burgerking.ca/store-locator/store/restaurant_11513', 'fast food', 1, '{ "mon": "0900-0500", "tue": "0900-0500", "wed": "0900-0500", "thu": "0900-0500", "fri": "0900-0500", "sat": "0900-0500", "sun": "0900-0500" }'),
('Ken’s Sushi', 'Sushi restaurant', 'Blair House, 256 Phillip St, Waterloo, ON N2L 6B6', '(519) 883-7272', 'https://www.kensushihouse.ca/', 'sushi', 3, '{ "mon": "1130-1500, 1600-2200", "tue": "1130-1500, 1600-2200", "wed": "1130-1500, 1600-2200", "thu": "1130-1500, 1600-2200", "fri": "1130-1500, 1600-2200", "sat": "1200-1500, 1600-2200", "sun": "1200-1500, 1600-2100" }');

INSERT INTO Items (item_id, item_name, restaurant_id, Price)
VALUES 
(1, 'Original Lanzhou Noodles', 1, 13.99),
(2, 'Royal Salmon Combo', 4, 26.00),
(3, '8 Piece Nuggets', 3, 3.99),
(4, 'Whopper', 3, 8.49),
(5, 'Whopper Combo', 3, 12.19),
(6, 'Roast Salmon Rice', 2, 13.99),
(7, 'Spicy Crispy Salmon Roll Combo', 2, 13.99);

INSERT INTO Discount (restaurant_id, item_id, discount, discount_type, weekday)
VALUES 
(1, NULL, 10.0, '%', 'tue'),
(3, 4, 2.5, '$', 'wed'),
(3, 5, 2.5, '$', 'wed');

INSERT INTO Reviews (restaurant_id, user_id, rating, comments, timestamp)
VALUES 
(2, 2, 5, 'sushi good', '2024-06-01 00:00:00'),
(3, 2, 5, 'whopper wednesday banger', '2024-06-02 00:00:00'),
(2, 1, 1, 'SUSHI GAVE ME FOOD POISONING', '2024-06-05 00:00:00');

INSERT INTO Favorites (user_id, restaurant_id)
VALUES 
(2, 2),
(3, 1);
