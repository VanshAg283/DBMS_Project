-- Triggers

-- 1. Trigger to Update Likes Count in Portfolio Table
DELIMITER //
CREATE TRIGGER update_likes_count AFTER INSERT ON Likes
FOR EACH ROW
BEGIN
    UPDATE Portfolio p
    SET likes = (
        SELECT COUNT(l.productID)
        FROM Likes l
        WHERE l.productID IN (
            SELECT productID
            FROM Product
            WHERE portfolioID = p.portfolioID
        )
    )
    WHERE p.portfolioID IN (
        SELECT portfolioID
        FROM Product
        WHERE productID = NEW.productID
    );
END;
//
DELIMITER ;

-- 2. Trigger to Update Total Price in Cart Table
DELIMITER //
CREATE TRIGGER update_cart_total_price AFTER INSERT ON CartItem
FOR EACH ROW
BEGIN
    UPDATE Cart c
    SET totalPrice = (
        SELECT SUM(ci.price * ci.quantity)
        FROM CartItem ci
        WHERE ci.cartID = c.cartID
    )
    WHERE c.cartID = NEW.cartID;
END;
//
DELIMITER ;

-- 3. Trigger to Check Maximum Units Cap
DELIMITER //
CREATE TRIGGER check_max_units BEFORE INSERT ON CartItem
FOR EACH ROW
BEGIN
    DECLARE max_units_cap INT;
    
    SELECT maxUnitsCap INTO max_units_cap
    FROM Product
    WHERE productID = NEW.cartItemID;
    
    IF NEW.quantity > max_units_cap THEN
        SET @error_message = CONCAT('Quantity exceeds maximum units cap (', max_units_cap, ') for product.');
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = @error_message;
    END IF;
END;
//
DELIMITER ;

-- 4. Trigger to Enforce Unique Email in Customer Table
DELIMITER //
CREATE TRIGGER enforce_unique_email BEFORE INSERT ON Customer
FOR EACH ROW
BEGIN
    DECLARE email_count INT;
    SELECT COUNT(*) INTO email_count
    FROM Customer
    WHERE email = NEW.email;
    
    IF email_count > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Email already exists in the database';
    END IF;
END;
//
DELIMITER ;

-- 5. Trigger to Update Available Units in Product Table
DELIMITER //
CREATE TRIGGER update_available_units AFTER INSERT ON CartItem
FOR EACH ROW
BEGIN
    DECLARE remaining_units INT;
    
    SELECT (p.availableUnits - NEW.quantity) INTO remaining_units
    FROM Product p
    WHERE p.productID = NEW.cartItemID;
    
    IF remaining_units < 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Not enough units available for product';
    ELSE
        UPDATE Product
        SET availableUnits = remaining_units
        WHERE productID = NEW.cartItemID;
    END IF;
END;
//
DELIMITER ;


-- 6. Trigger to Update Login Attempts and Block Customer
DELIMITER //

CREATE TRIGGER update_login_attempts
AFTER INSERT ON LoginAttempts
FOR EACH ROW
BEGIN
    UPDATE Customer
    SET login_attempts = login_attempts + 1
    WHERE custName = NEW.customer_id;
    
    -- Check if the login attempts exceed the threshold
    IF (SELECT login_attempts FROM Customer WHERE custName = NEW.customer_id) >= 3 THEN
        -- Update the blocked status to true
        UPDATE Customer
        SET blocked = TRUE
        WHERE custName = NEW.customer_id;
    END IF;
END;
//

DELIMITER ;


-- 7. Trigger to Update Login Attempts on Successful Login
DELIMITER //

CREATE TRIGGER reset_login_attempts
AFTER DELETE ON LoginAttempts
FOR EACH ROW
BEGIN
    DECLARE customer_id VARCHAR(30);
    
    -- Get the customer_id of the deleted row
    SET customer_id = OLD.customer_id;
    
    -- Reset login_attempts to 0 and set blocked to false for the corresponding customer
    UPDATE Customer
    SET login_attempts = 0,
        blocked = FALSE
    WHERE custName = customer_id;
END;
//

DELIMITER ;



