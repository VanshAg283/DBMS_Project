-- For Order 'O001'
INSERT INTO Transaction (transactionID, discountID, custName, orderID)
VALUES ('T001', 'D01', 'eum', 'O001');

-- For Order 'O002'
INSERT INTO Transaction (transactionID, discountID, custName, orderID)
VALUES ('T002', 'D02', 'ullam', 'O002');

-- For Order 'O003'
INSERT INTO Transaction (transactionID, discountID, custName, orderID)
VALUES ('T003', 'D03', 'atque', 'O003');

-- For Order 'O004'
INSERT INTO Transaction (transactionID, discountID, custName, orderID)
VALUES ('T004', 'D04', 'commodi', 'O004');

-- For Order 'O005'
INSERT INTO Transaction (transactionID, discountID, custName, orderID)
VALUES ('T005', 'D05', 'id', 'O005');

-- For Order 'O006'
INSERT INTO Transaction (transactionID, discountID, custName, orderID)
VALUES ('T006', 'D06', 'occaecati', 'O006');


-- Update transactionPrice in Transaction table
UPDATE Transaction t
SET transactionPrice = (
    SELECT (c.totalPrice - (c.totalPrice * d.discountPercent / 100))
    FROM Cart c
    JOIN Discount d ON t.discountID = d.discountID
    JOIN `Order` o ON t.orderID = o.orderID
    WHERE o.cartID = c.cartID
);
