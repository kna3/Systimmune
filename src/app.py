import os
import sys
import mysql.connector
import csv
from flask import Flask, request, render_template
from flask_mysqldb import MySQL
import setup, argparse

#Initialize Flask application
app = Flask(__name__)

#Parse input files from Command Line 
parser=argparse.ArgumentParser(description="")
parser.add_argument('-f1', required=True)
parser.add_argument('-f2', required=True)
parser.add_argument('-f3', required=True)
parser.add_argument('-f4', required=True)
parser.add_argument('-f5', required=True)
parser.add_argument('-f6', required=True)
args=vars(parser.parse_args())

file1=args["f1"]
file2=args["f2"]
file3=args["f3"]
file4=args["f4"]
file5=args["f5"]
file6=args["f6"]

#Invoke function to setup database and add data to tables
def setupDatabase():
    setup.create(file1,file2,file3,file4,file5,file6)
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
    bestSalesPerson = setup.getBestSalesperson(startDate, endDate)
    topModel= setup.getTopModel(startDate, endDate)
    noSalesPerson = None
    noTopModel = None
    if not bestSalesPerson:
        noSalesPerson = True
    if not topModel:
        noTopModel = True

    return render_template("index.html", salesmanName=bestSalesPerson, modelName = topModel, hasBestSalesPerson = noSalesPerson, hasTopModel = noTopModel)

if __name__ == '__main__':
    setupDatabase()
