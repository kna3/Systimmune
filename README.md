1. TO RUN THE PROJECT:
The project can be run from command-line terminal using the command:

	python app.py -f1 vehicle.csv -f2 inventory.csv -f3 salesperson.csv -f4 branch.csv -f5 carsold.csv -f6 customer.csv

We validate the arguments by ensuring that all the 6 parameters are passed, otherwise it will return an error.
The dummy data is added manually to the all csv files to maintain a clear understanding of the working of the project. The reference can be taken from the CarSold table to ensure consistency of the result.

2. There are Six Tables for the Database CarDealership namely 
-Vehicle(id, name, model, miles, price)
 Contains information about the vehicle

-Inventory(id, vehicle_id, is_sold, state, description, title)
 Contains information of a specific inventory and the condition of the vehicle

-SalesPerson(id, name, phone, branch_location)
 Information about the salesPerson
 
-Branch(location,code)
 City of the Car Dealership Branch

-CarSold(sale_id, vehicle_id, salesperson_id, date_sold)
 Contains Information about all the cars that were sold and the date of the deal

-Customer(id, name, branch_code)
 Information of Customers who bought the car

The File Structure is as below:
	/Systimmune
		/src
		setup.py
		app.py
		config.txt
		     /templates
		      index.html
		     /static
			   /css
			    index.css	
			   /icons

3. The DataBase related queries are done in 'setup.py' file. The credentials required to establish database connection are stored in a config.txt file.
We create a Database with the name CarDealership
We define the schema by using 'create table' sql queries for the six tables
While loading the data we carry out data validation using try and except block by cross-validating the data from the csv file to the database scheme that was defined. If a field in csv is incorrect, that record is not added into the database and the error statement is logged accordingly with the line number.
Intially I was using LOAD DATA INFILE to insert the data into the tables quickly but it doesn't support data validation, so I used the 'INSERT INTO tablename' query to insert and validate the data.

4. After successfully loading the data, we run the query to find out the top model(getTopModel) and the top salesman(getBestSalesperson) for the month and return the data to be displayed by rendering index.html template.

5. In 'app.py' file, we initialize our Flask application which is used to create a server and upload results on the web page. We intake the filenames from command line using the arguement parser and then call the function in setup.py to trigger the database queries. We render the index.html file to display the home page. We use a form to take input from the user (start date and end date). The start and the end date are passed to the getTopModel and getBestSalesperson and then display it on the Web Page on the '/sendDate' route. We enable the html to display a list of output if the query returns more than one results i.e. two models having the same count or two salesperson selling equal number of cars in a period. If there is no result from the query it shows "No car was sold in this period and best Sales Person cannot be calculated"

6. We use CSS, BootStrap and HTML to display the results. The website has been created using flexbox that allows creating a responsive web application.

7. The project is not just limited to display results for a specific month but any requested time period.
