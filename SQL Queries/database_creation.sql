create database DesInk;
use DesInk;

CREATE TABLE Designer (
    desName varchar(10) NOT NULL,
    email varchar(30) NOT NULL,
    password varchar(8) NOT NULL,
    firstName varchar(20) NOT NULL,
    lastName varchar(20) NOT NULL,
    fullName varchar(40) generated always as (concat(firstName,' ',lastName)) stored,
    portfolioID varchar(10) NOT NULL,
    PRIMARY KEY (desName),
    UNIQUE (email)
);

CREATE TABLE Portfolio(
    portfolioID varchar(10) NOT NULL,
    likes bigint unsigned NOT NULL DEFAULT 0,
    preOrders int unsigned NOT NULL DEFAULT 0,
    desName varchar(10) NOT NULL,
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
    productID int unsigned NOT NULL,
    title varchar(15) NOT NULL,
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
    custName varchar(10) NOT NULL,
    email varchar(40) NOT NULL,
    password varchar(8) NOT NULL,
    firstName varchar(20) NOT NULL,
    lastName varchar(20) NOT NULL,
    fullName varchar(40) generated always as (concat(firstName,' ',lastName)) stored,
    PRIMARY KEY (custName),
    UNIQUE (email)
);

CREATE TABLE Cart(
    cartID varchar(10) NOT NULL,
    custName varchar(10) NOT NULL,
    totalPrice float(2) NOT NULL,
    PRIMARY KEY (cartID),
    FOREIGN KEY (custName)
    REFERENCES customer(custName)
    ON DELETE CASCADE
    ON UPDATE CASCADE 
);

CREATE TABLE Places (
    transactionID varchar(10) NOT NULL,
    discountID varchar(10) NOT NULL,
    custName varchar(10) NOT NULL,
    orderID varchar(10) NOT NULL
);

CREATE TABLE Includedin (
  cartID varchar(10) NOT NULL,
  productID varchar(10) NOT NULL
);

CREATE TABLE Order (
    orderID varchar(10) NOT NULL,
    orderDate date NOT NULL,
    delStatus varchar(15) NOT NULL,
    custName varchar(10) NOT NULL,
    addressID varchar(10) NOT NULL,
    PRIMARY KEY (orderID),
    FOREIGN KEY (custName) REFERENCES customer(custName),
    FOREIGN KEY (addressID) REFERENCES Address(addressID)
);

CREATE TABLE Address(
    addressID varchar(10) NOT NULL,
    houseNo varchar(5) NOT NULL,
    street varchar(5) NOT NULL,
    city varchar(10) NOT NULL,
    state varchar(10) NOT NULL,
    pincode varchar(7) NOT NULL,
    PRIMARY KEY (addressID)
);


CREATE TABLE Discount (
  discountID varchar(10),
  discountCode varchar(10),
  discountPercent integer,
  expirationDate date
);

CREATE TABLE CartItem (
    cartItemID varchar(10) NOT NULL,
    cartID varchar(10) NOT NULL,
    price float(2) NOT NULL,
    quantity int NOT NULL,
    dateAdded date NOT NULL,
    PRIMARY KEY ()
)