CREATE DATABASE car_showroom;

USE car_showroom;

CREATE TABLE Cars (
    Car_ID VARCHAR(10) PRIMARY KEY,
    Brand VARCHAR(50),
    Model VARCHAR(50),
    Year INT,
    Color VARCHAR(30),
    Engine_Type VARCHAR(30),
    Transmission VARCHAR(30),
    Price FLOAT,
    Quantity_In_Stock INT,
    Status VARCHAR(30)
);

CREATE TABLE Customers (
    Customer_ID VARCHAR(10) PRIMARY KEY,
    Name VARCHAR(100),
    Gender VARCHAR(10),
    Age INT,
    Phone VARCHAR(20),
    Email VARCHAR(100),
    City VARCHAR(100)
);

CREATE TABLE Sales (
    Sale_ID VARCHAR(10) PRIMARY KEY,
    Customer_ID VARCHAR(10),
    Car_ID VARCHAR(10),
    Sale_Date DATE,
    Quantity INT,
    Sale_Price FLOAT,
    Payment_Method VARCHAR(50),
    Salesperson VARCHAR(100),
    FOREIGN KEY (Customer_ID) REFERENCES Customers(Customer_ID),
    FOREIGN KEY (Car_ID) REFERENCES Cars(Car_ID)
);