UPDATE Restaurants
SET price_range = (
    SELECT CASE
        WHEN avg_price < 15 THEN 1
        WHEN avg_price BETWEEN 15 AND 25 THEN 2
        ELSE 3
    END
    FROM (
        SELECT AVG(price) as avg_price
        FROM Items
        WHERE restaurant_id = Restaurants.restaurant_id
    ) as avg_prices
);