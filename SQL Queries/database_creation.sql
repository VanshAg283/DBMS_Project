DROP DATABASE IF EXISTS DesInk;
create database DesInk;
use DesInk;

CREATE TABLE Designer (
    desName varchar(30) NOT NULL,
    email varchar(50) NOT NULL,
    password varchar(10) NOT NULL,
    firstName varchar(20) NOT NULL,
    lastName varchar(20) NOT NULL,
    fullName varchar(40) generated always as (concat(firstName,' ',lastName)) stored,
    portfolioID varchar(10),
    PRIMARY KEY (desName),
    UNIQUE (email)
);

CREATE TABLE Portfolio(
    portfolioID varchar(10) NOT NULL,
    likes bigint unsigned NOT NULL DEFAULT 0,
    desName varchar(30),
    PRIMARY KEY (portfolioID),
    FOREIGN KEY (desName)
        REFERENCES Designer(desName)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

ALTER TABLE Designer
ADD CONSTRAINT Fk_Designer_portfolioID
FOREIGN KEY(portfolioID) 
REFERENCES Portfolio(portfolioID)
ON DELETE CASCADE
ON UPDATE CASCADE;

CREATE TABLE Product (
    productID varchar(10) NOT NULL,
    title varchar(30) NOT NULL,
    content varchar(50),
    category varchar(15) NOT NULL,
    price float(2) NOT NULL,
    availableUnits int unsigned NOT NULL,
    maxUnitsCap int unsigned NOT NULL,
    portfolioID varchar(10) NOT NULL,
    PRIMARY KEY (productID),
    FOREIGN KEY (portfolioID)
    REFERENCES Portfolio(portfolioID)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE Customer(
    custName varchar(30) NOT NULL,
    email varchar(50) NOT NULL,
    password varchar(10) NOT NULL,
    firstName varchar(20) NOT NULL,
    lastName varchar(20) NOT NULL,
    fullName varchar(40) generated always as (concat(firstName,' ',lastName)) stored,
    PRIMARY KEY (custName),
    UNIQUE (email)
);

CREATE TABLE Cart(
    cartID varchar(10) NOT NULL,
    custName varchar(30) NOT NULL,
    totalPrice float(2) DEFAULT 0,
    PRIMARY KEY (cartID),
    FOREIGN KEY (custName)
    REFERENCES customer(custName)
    ON DELETE CASCADE
    ON UPDATE CASCADE 
);

CREATE TABLE Address(
    addressID varchar(10) NOT NULL,
    houseNo varchar(5) NOT NULL,
    street varchar(30) NOT NULL,
    city varchar(30) NOT NULL,
    state varchar(30) NOT NULL,
    pincode varchar(7) NOT NULL,
    PRIMARY KEY (addressID)
);

CREATE TABLE Discount (
  discountID varchar(10) NOT NULL,
  discountCode varchar(10) NOT NULL,
  discountPercent int NOT NULL,
  expirationDate date,
  PRIMARY KEY (discountID)
);

CREATE TABLE `Order` (
    orderID INT AUTO_INCREMENT,
    orderDate DATE NOT NULL,
    delStatus VARCHAR(15) NOT NULL,
    custName VARCHAR(30) NOT NULL,
    addressID VARCHAR(10) NOT NULL,
    cartID VARCHAR(10) NOT NULL,
    discountID VARCHAR(10),
    PRIMARY KEY (orderID),
    FOREIGN KEY (custName) REFERENCES customer(custName),
    FOREIGN KEY (addressID) REFERENCES Address(addressID),
    FOREIGN KEY (cartID) REFERENCES Cart(cartID),
    FOREIGN KEY (discountID) REFERENCES Discount(discountID)
);

CREATE TABLE CartItem (
    cartItemID varchar(10) NOT NULL,
    cartID varchar(10) NOT NULL,
    price float(2) NOT NULL,
    quantity int NOT NULL,
    dateAdded date NOT NULL,
    PRIMARY KEY (cartItemID,cartID),
    FOREIGN KEY (cartItemID) references Product(productID),
    FOREIGN KEY (cartID) references Cart(cartID)
);

CREATE TABLE Transaction (
    transactionID INT AUTO_INCREMENT PRIMARY KEY,
    discountID varchar(10) NOT NULL,
    custName varchar(30) NOT NULL,
    orderID INT NOT NULL,
    transactionPrice float(2),
    FOREIGN KEY (discountID) REFERENCES Discount(discountID),
    FOREIGN KEY (custName) REFERENCES Customer(custName),
    FOREIGN KEY (orderID) REFERENCES `Order`(orderID)
);

CREATE TABLE Includedin (
  cartID varchar(10) NOT NULL,
  productID varchar(10) NOT NULL,
  FOREIGN KEY (cartID) references Cart(cartID),
  FOREIGN KEY (productID) references Product(productID)
);

CREATE TABLE Likes (
  custName varchar(30) NOT NULL,
  productID varchar(10) NOT NULL,
  FOREIGN KEY (custName) references Customer(custName),
  FOREIGN KEY (productID) references Product(productID) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE LoginAttempts (
     id INT AUTO_INCREMENT PRIMARY KEY,
     customer_id varchar(30) NOT NULL,
     login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
     FOREIGN KEY (customer_id) REFERENCES Customer(custName)
);

ALTER TABLE Customer
ADD COLUMN login_attempts INT DEFAULT 0,
ADD COLUMN blocked BOOLEAN DEFAULT FALSE;