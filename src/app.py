import os
import sys
import mysql.connector
import csv
from flask import Flask, request, render_template
from flask_mysqldb import MySQL
import setup, argparse

#Initialize Flask application
app = Flask(__name__)

#Invoke function to setup database and add data to tables
def setupDatabase():
    setup.create()
    app.run()

#Method to render index.html 
@app.route('/', methods = ['GET'])
def hello():
    return render_template("index.html")

#Method to fetch month from the Web Page    
@app.route('/sendDate', methods=['POST'])
def sendDate():
    startDate = request.form.get('start_date')
    endDate = request.form.get('end_date')
    data = setup.getBestSalesperson(startDate, endDate)
    data2= setup.getTopModel(startDate, endDate)

    return render_template("index.html", salesmanName=data, modelName = data2)

if __name__ == '__main__':
    setupDatabase()
