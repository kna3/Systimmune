import mysql.connector

#Establish connection with the MySQL Server	
mydb = mysql.connector.connect(host = "localhost",user = "root", password = "1234")

#Cursor to execute SQL queries
mycursor = mydb.cursor()

#Creating the Database
mycursor.execute("CREATE DATABASE IF NOT EXISTS CarDealership")

mycursor.execute("USE CarDealership")


def create():

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

	mycursor.execute("SET @@GLOBAL.local_infile = 1")

#Populate data from local csv files into table
	mycursor.execute("LOAD DATA LOCAL INFILE 'vehicle.csv' INTO TABLE Vehicle FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 LINES (vehicle_id, vehicle_name, vehicle_model, miles_completed, vehicle_price)")

	mycursor.execute("LOAD DATA LOCAL INFILE 'inventory.csv' INTO TABLE Inventory FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 LINES (inventory_id, vehicle_id, is_sold, vehicle_state, inventory_description, inventory_title, branch_location)")

	mycursor.execute("LOAD DATA LOCAL INFILE 'salesperson.csv' INTO TABLE Salesperson FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 LINES (salesperson_id, salesperson_name, salesperson_phone, branch_location)")

	mycursor.execute("LOAD DATA LOCAL INFILE 'branch.csv' INTO TABLE Branch FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 LINES (branch_location, branch_code)")

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

#Close connection
mycursor.close()
