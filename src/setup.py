import mysql.connector
import csv
from flask import jsonify
import configparser
import MySQLdb
from itertools import islice

#Take Credentials from config.txt
config = configparser.ConfigParser()
config.readfp(open(r'config.txt'))
user = config.get('My_Config','USERNAME')
host = config.get('My_Config','HOST')
password = config.get('My_Config','PASSWORD')

#Establish connection with the MySQL Server	
mydb = mysql.connector.connect(host = host ,user = user, password = password)

#Cursor to execute SQL queries
mycursor = mydb.cursor()

#Creating the Database
mycursor.execute("CREATE DATABASE IF NOT EXISTS CarDealership")

mycursor.execute("USE CarDealership")


def create(file1,file2,file3,file4,file5,file6):

	#Creating the Table Vehicle in CarDealership Database
	mycursor.execute("CREATE TABLE IF NOT EXISTS Vehicle (vehicle_id INT(20) Primary Key AUTO_INCREMENT,vehicle_name VARCHAR(30) NOT NULL,vehicle_model INT(4) NOT NULL,miles_completed INT(15) default 0,vehicle_price DECIMAL(10,2) )")

	#Creating the Table Inventory in CarDealership Database
	mycursor.execute("CREATE TABLE IF NOT EXISTS Inventory (inventory_id INT(20) Primary Key AUTO_INCREMENT,vehicle_id INT(30) NOT NULL,is_sold boolean default false,vehicle_state ENUM('New','Used') NOT NULL,inventory_description VARCHAR(50),inventory_title ENUM('Clean','Rebuilt','Salvage') NOT NULL,branch_location VARCHAR(30) NOT NULL)")

	mycursor.execute("CREATE TABLE IF NOT EXISTS SalesPerson (salesperson_id INT(20) Primary Key AUTO_INCREMENT,salesperson_name VARCHAR(30),salesperson_phone INT(30),branch_location VARCHAR(30))")

	mycursor.execute("CREATE TABLE IF NOT EXISTS Branch (branch_code INT(20) NOT NULL, branch_location VARCHAR(30))")

	mycursor.execute("CREATE TABLE IF NOT EXISTS Carsold (sale_id INT(30) Primary Key AUTO_INCREMENT,vehicle_id INT(20) NOT NULL, salesperson_id INT(20) NOT NULL,customer_id INT(20),date_sold DATE NOT NULL)")

	mycursor.execute("CREATE TABLE IF NOT EXISTS Customer (customer_id INT(30) Primary Key AUTO_INCREMENT,customer_name VARCHAR(30),branch_code INT(20))")

	mycursor.execute("SET @@GLOBAL.local_infile = 1")

	try:
		with open(file1) as csvfile:
			readCSV = csv.reader(csvfile, delimiter=',')
			for row in islice(readCSV, 1, None):
				val = (row[1],row[2],row[3],row[4])
				try:
					mycursor.execute("INSERT INTO Vehicle (vehicle_name,vehicle_model,miles_completed,vehicle_price) VALUES (%s,%s,%s,%s)",val)
					mydb.commit()
				except (mysql.connector.Error) as e:
					print(e)

		with open(file2) as csvfile:
			readCSV = csv.reader(csvfile, delimiter=',')
			for row in islice(readCSV, 1, None):
				val = (row[1],row[2],row[3],row[4],row[5],row[6])
				try:
					mycursor.execute("INSERT INTO Inventory (vehicle_id, is_sold, vehicle_state, inventory_description, inventory_title, branch_location) VALUES (%s,%s,%s,%s,%s,%s)",val)
					mydb.commit()
				except (mysql.connector.Error) as e:
					print(e)

		with open(file3) as csvfile:
			readCSV = csv.reader(csvfile, delimiter=',')
			for row in islice(readCSV, 1, None):
				val = (row[1],row[2],row[3])
				try:
					mycursor.execute("INSERT INTO Salesperson (salesperson_name, salesperson_phone, branch_location) VALUES (%s,%s,%s)",val)
					mydb.commit()
				except (mysql.connector.Error) as e:
					print(e)

		with open(file4) as csvfile:
			readCSV = csv.reader(csvfile, delimiter=',')
			for row in islice(readCSV, 1, None):
				val = (row[0],row[1])
				try:
					mycursor.execute("INSERT INTO Branch (branch_code, branch_location) VALUES (%s,%s)",val)
					mydb.commit()
				except (mysql.connector.Error) as e:
					print(e)	

		with open(file5) as csvfile:
			readCSV = csv.reader(csvfile, delimiter=',')
			for row in islice(readCSV, 1, None):
				val = (row[1],row[2],row[3],row[4])
				try:
					mycursor.execute("INSERT INTO Carsold (vehicle_id, salesperson_id, customer_id, date_sold) VALUES (%s,%s,%s,%s)",val)
					mydb.commit()
				except (mysql.connector.Error) as e:
					print(e)

		with open(file6) as csvfile:
			readCSV = csv.reader(csvfile, delimiter=',')
			for row in islice(readCSV, 1, None):
				val = (row[1],row[2])
				try:
					mycursor.execute("INSERT INTO Customer (customer_name, branch_code) VALUES (%s,%s)",val)
					mydb.commit()
				except (mysql.connector.Error) as e:
					print(e)

    # a = f"LOAD DATA LOCAL INFILE '{file1}' INTO TABLE Vehicle FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 LINES (vehicle_id, vehicle_name, vehicle_model, miles_completed, vehicle_price)"
	# mycursor.execute(a)
	# b = f"LOAD DATA LOCAL INFILE '{file2}' INTO TABLE Inventory FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 LINES (inventory_id, vehicle_id, is_sold, vehicle_state, inventory_description, inventory_title, branch_location)"
	# mycursor.execute(b)
	# c =f"LOAD DATA LOCAL INFILE '{file3}' INTO TABLE Salesperson FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 LINES (salesperson_id, salesperson_name, salesperson_phone, branch_location)"
	# mycursor.execute(c)
	# d = f"LOAD DATA LOCAL INFILE '{file4}' INTO TABLE Branch FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 LINES (branch_location, branch_code)"
	# mycursor.execute(d)
	# e = f"LOAD DATA LOCAL INFILE '{file5}' INTO TABLE Carsold FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 LINES (sale_id, vehicle_id, salesperson_id, customer_id, date_sold)"
	# mycursor.execute(e)
	except (MySQLdb.Error, MySQLdb.Warning) as e:
		print(e)

	mydb.commit()

#Function to find the top salesman for the specific month
def getBestSalesperson(startDate, endDate):
	query = f"select s.salesperson_name, count(*) as ct from carsold c join salesperson s on c.salesperson_id = s.salesperson_id where c.date_sold between '{startDate}' and '{endDate}' group by c.salesperson_id having ct = (select max(ct) from (select count(*) as ct from carsold where date_sold between '{startDate}' and '{endDate}' group by salesperson_id) as a)"
	mycursor.execute(query)
	result = mycursor.fetchall()
	salesPersonArray = []
	content = {}
	for res in result:
		content = {'salesPersonName': res[0], 'count': res[1]}
		salesPersonArray.append(content)
		content = {}
	return salesPersonArray

#Function to find the top Car Model for the specific month
def getTopModel(startDate, endDate):
	query = f"select vehicle_name, vehicle_model, count(*) as c from vehicle v join carsold cs where v.vehicle_id = cs.vehicle_id and date_sold between '{startDate}' and '{endDate}' group by vehicle_name, vehicle_model having c = (select max(c) from (select count(*) as c from carsold where date_sold between '{startDate}' and '{endDate}'  group by vehicle_id) as a)"
	mycursor.execute(query)
	result = mycursor.fetchall()
	modelArray = []
	content = {}
	for res in result:
		content = {'vehicleName': res[0], 'vehicleModel': res[1], 'vehicleCount': res[2]}
		modelArray.append(content)
		content = {}
	return modelArray
