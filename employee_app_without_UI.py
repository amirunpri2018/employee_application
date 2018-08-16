from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy import Column, DateTime
from flask_cors import CORS, cross_origin
# I have imported cors because swagger was not able to post

app = Flask(__name__)
CORS(app, support_credentials=True)

database_parameters = 'mysql://root:prasad123@localhost:3306/employees'
app.config['SQLALCHEMY_DATABASE_URI'] = database_parameters
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# let me know the changes in the database but i don't want to know, just
# setting some value (False) to avoid overhead warning

# create database object for the respective flask app
db = SQLAlchemy(app)


# class in flask will be representing table in database
class Employee(db.Model):
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    id = db.Column(db.Integer, primary_key=True)  # This is my primary key
    name = db.Column(db.String(200))
    designation = db.Column(db.String(200))
    mobile_number = db.Column(db.String(200))
    email_id = db.Column(db.String(200))


# This api will give all employees details
@app.route('/')   # http://127.0.0.1:5000/
@cross_origin(supports_credentials=True)
def index():
    all_data = Employee.query.all()  # Gives all data from Employee table
    employees = []
    for field in all_data:
        employees.append(
            {
                'id': field.id,
                'name': field.name,
                'designation': field.designation,
                'mobile_number': field.mobile_number,
                'email_id': field.email_id
            })

    all_employees = jsonify({'employees': employees})
    return all_employees


# This api will adds/process new employee details
@app.route('/add', methods=['POST'])  # http://127.0.0.1:5000/add
@cross_origin(supports_credentials=True)
def add():
    # accessing posted data
    name = request.json['name']
    designation = request.json['designation']
    mobile_number = request.json['mobile_number']
    email_id = request.json['email_id']

    # now save the data in database (pk will be auto incremented)
    employee_details = Employee(name=name, designation=designation,
                                mobile_number=mobile_number, email_id=email_id)
    # adds the employee data into db session
    db.session.add(employee_details)
    db.session.commit()                 # and then save the data in database

    all_data = Employee.query.all()  # Gives all data from Employee table
    employees = []
    for field in all_data:
        employees.append(
            {
                'id': field.id,
                'name': field.name,
                'designation': field.designation,
                'mobile_number': field.mobile_number,
                'email_id': field.email_id
            })

    all_employess = jsonify({'employees': employees})
    return all_employess


# This api will update the existing details of employee
@app.route('/update', methods=['GET', 'POST'])  # http://127.0.0.1:5000/update
@cross_origin(supports_credentials=True)
def update():
    if request.method == 'POST':
        # extracting the ID of the employee from the POST request
        employee_id = request.json['id']

        employee_update = Employee.query.get(employee_id)
        employee_update.name = request.json['name']
        employee_update.designation = request.json['designation']
        employee_update.mobile_number = request.json['mobile_number']
        employee_update.email_id = request.json['email_id']

        db.session.commit()  # Save the updated changes in db

        all_data = Employee.query.all()  # Gives all data from Employee table
        employees = []
        for field in all_data:
            employees.append(
                {
                    'id': field.id,
                    'name': field.name,
                    'designation': field.designation,
                    'mobile_number': field.mobile_number,
                    'email_id': field.email_id
                })

        all_employess = jsonify({'employees': employees})
        return all_employess


# This api will delete the existing employee
@app.route('/delete', methods=['POST'])  # http://127.0.0.1:5000/delete
@cross_origin(supports_credentials=True)
def delete():
    employee_id = request.json['id']
    employee = Employee.query.get(employee_id)
    db.session.delete(employee)
    db.session.commit()

    # After deleting the record, show the home page
    all_data = Employee.query.all()  # Gives all data from Employee table
    employees = []
    for field in all_data:
        employees.append(
            {
                'id': field.id,
                'name': field.name,
                'designation': field.designation,
                'mobile_number': field.mobile_number,
                'email_id': field.email_id
            })

    all_employess = jsonify({'employees': employees})
    return all_employess


if __name__ == '__main__':
    app.run(debug=True)
