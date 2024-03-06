-- SQL Queries

-- 1. Calculate Average Price for Each Category
SELECT category, AVG(price) AS avgPrice
FROM Product
GROUP BY category;


-- 2. Check products without any likes
SELECT p.productID, p.title
FROM Product p
WHERE NOT EXISTS (
    SELECT 1
    FROM Likes l
    WHERE l.productID = p.productID
);


-- 3. Update Discount Expiration Date
UPDATE Discount
SET expirationDate = DATE_SUB(expirationDate, INTERVAL 31 DAY)


-- 4. Remove Discount for Expired Discounts:
DELETE FROM Discount
WHERE expirationDate < CURDATE();


-- 5. Delete Designer and Associated Portfolio along with products and likes
DELETE FROM Designer
WHERE desName = 'ullam';


-- 6. Arrange in decreasing order of how many times a customer have placed orders
SELECT custName, COUNT(orderID) AS orderCount
FROM `Order`
NATURAL JOIN Customer
GROUP BY custName
ORDER BY orderCount DESC;


-- 7. Retrieve products that have not been liked by any customer
SELECT p.*
FROM Product p
LEFT JOIN Likes l ON p.productID = l.productID
WHERE l.productID IS NULL;


-- 8.  Calculate the total revenue for each month in the year 2024:
SELECT MONTH(`Order`.orderDate) AS order_month, SUM(`Transaction`.transactionPrice) AS total_revenue
FROM `Order`
JOIN Transaction ON `Order`.orderID = Transaction.orderID
WHERE YEAR(`Order`.orderDate) = "2024"
GROUP BY order_month;


-- 9. Arrange Designers on basis of their Highest Total Order Value
SELECT d.desName, d.fullName, SUM(p.price * ci.quantity) AS totalOrderValue
FROM Designer d
JOIN Portfolio po ON d.portfolioID = po.portfolioID
JOIN Product p ON po.portfolioID = p.portfolioID
JOIN CartItem ci ON p.productID = ci.cartItemID
JOIN `Order` o ON ci.cartID = o.cartID
GROUP BY d.desName
ORDER BY totalOrderValue DESC;


-- 10. Update available units of product from ordered items
UPDATE Product
SET availableUnits = availableUnits - COALESCE((
    SELECT SUM(quantity)
    FROM `Order` o
    JOIN Cart ca ON o.cartID = ca.cartID
    JOIN CartItem ci ON ca.cartID = ci.cartID
    WHERE ci.cartItemID = Product.productID
), 0);