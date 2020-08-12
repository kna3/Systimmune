import mysql.connector

#Establish connection with the MySQL Server
mydb = mysql.connector.connect(host = "localhost",user = "root", password = "1234")

#Cursor to execute SQL queries
mycursor = mydb.cursor()

#Creating the Database
mycursor.execute("CREATE DATABASE IF NOT EXISTS CarDealership")

mycursor.execute("USE CarDealership")

#Creating the Table Vehicle in CarDealership Database
mycursor.execute("CREATE TABLE IF NOT EXISTS Vehicle (vehicle_id INT(20) PRIMARY KEY,vehicle_name VARCHAR(30) NOT NULL,vehicle_model INT(4) NOT NULL,miles_completed INT(15) default 0,vehicle_price DECIMAL(10,2) NOT NULL )")

#Creating the Table Inventory in CarDealership Database
mycursor.execute("CREATE TABLE IF NOT EXISTS Inventory (inventory_id INT(20) NOT NULL,vehicle_id INT(30) NOT NULL,is_sold boolean default false,vehicle_state ENUM('New','Used') NOT NULL,inventory_description VARCHAR(50),inventory_title ENUM('Clean','Rebuilt','Salvage'),branch_location VARCHAR(30) NOT NULL)")

#Creating the Table SalesPerson in CarDealership Database
mycursor.execute("CREATE TABLE IF NOT EXISTS SalesPerson (salesperson_id INT(20) NOT NULL,salesperson_name VARCHAR(30),salesperson_phone INT(10),branch_location VARCHAR(30))")

#Creating the Table Branch in CarDealership Database
mycursor.execute("CREATE TABLE IF NOT EXISTS Branch (branch_location VARCHAR(30),branch_code INT(20))")

#Creating the Table CarSold in CarDealership Database
mycursor.execute("CREATE TABLE IF NOT EXISTS CarSold (sale_id INT(30),vehicle_id INT(20), salesperson_id INT(20),customer_id INT(20),date_sold DATE NOT NULL)")