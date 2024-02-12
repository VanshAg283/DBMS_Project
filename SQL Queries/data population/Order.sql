INSERT INTO `Order` (orderID, orderDate, delStatus, custName, addressID, cartID) VALUES ('O001', '2024-01-21', 'Preordered', 'eum', 'A001', 'C01');
INSERT INTO `Order` (orderID, orderDate, delStatus, custName, addressID, cartID) VALUES ('O002', '2024-01-22', 'Processing', 'ullam', 'A002', 'C02');
INSERT INTO `Order` (orderID, orderDate, delStatus, custName, addressID, cartID) VALUES ('O003', '2024-01-23', 'Shipped', 'atque', 'A003', 'C03');
INSERT INTO `Order` (orderID, orderDate, delStatus, custName, addressID, cartID) VALUES ('O004', '2024-01-24', 'Preordered', 'commodi', 'A004', 'C04');
INSERT INTO `Order` (orderID, orderDate, delStatus, custName, addressID, cartID) VALUES ('O005', '2024-01-25', 'Delivered', 'id', 'A005', 'C05');
INSERT INTO `Order` (orderID, orderDate, delStatus, custName, addressID, cartID) VALUES ('O006', '2024-01-26', 'Shipped', 'occaecati', 'A006', 'C06');

UPDATE `Order` SET discountID = 'D01' WHERE cartID = 'C01';
UPDATE `Order` SET discountID = 'D02' WHERE cartID = 'C02';
UPDATE `Order` SET discountID = 'D03' WHERE cartID = 'C03';
UPDATE `Order` SET discountID = 'D04' WHERE cartID = 'C04';
UPDATE `Order` SET discountID = 'D05' WHERE cartID = 'C05';
UPDATE `Order` SET discountID = 'D06' WHERE cartID = 'C06';