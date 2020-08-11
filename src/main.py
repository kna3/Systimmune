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