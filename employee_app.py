from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy import Column, DateTime


app = Flask(__name__)

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
def index():
    all_data = Employee.query.all()  # Gives all data from Employee table
    return render_template('home.html', all_data=all_data)


# This url will be redirecting the page only
@app.route('/add')   # http://127.0.0.1:5000/add
def add():           # This url will be redirected
    return render_template('add_employee.html')


# This api will adds/process new employee details
@app.route('/process', methods=['POST'])  # http://127.0.0.1:5000/process
def process():
    # accessing posted data
    name = request.form['name']
    designation = request.form['designation']
    mobile_number = request.form['mobile_number']
    email_id = request.form['email_id']
    print name, designation, mobile_number, email_id

    # now save the data in database (pk will be auto incremented)
    employee_details = Employee(name=name, designation=designation,
                                mobile_number=mobile_number, email_id=email_id)
    # adds the employee data into db session
    db.session.add(employee_details)
    db.session.commit()                 # and then save the data in database
    return redirect(url_for('index'))   # redirects to the view for /index


# This api will update the existing details of employee
@app.route('/update', methods=['GET', 'POST'])  # http://127.0.0.1:5000/update
def update():
    # when the request is post, update the employee data
    if request.method == 'POST':
        # extracting the ID of the employee from the POST request
        post_request_data = request.values
        employee_id = post_request_data['id'][0]

        employee_update = Employee.query.get(employee_id)
        employee_update.name = request.form['name']
        employee_update.designation = request.form['designation']
        employee_update.mobile_number = request.form['mobile_number']
        employee_update.email_id = request.form['email_id']

        db.session.commit()  # Save the changes in db

        # Now after editing show the home page to see the updated info
        all_data = Employee.query.all()  # Gives all data from Employee table
        return render_template('home.html', all_data=all_data)
    else:  # GET request is for showing the existing details of employee
        get_request_data = request.values
        employee_id = get_request_data['id'][0]
        # Now I have to get the Employees record having id=employee_id

        requested_employee_object = Employee.query.get(employee_id)
        employee_name = requested_employee_object.name
        employee_designation = requested_employee_object.designation
        employee_mobile_number = requested_employee_object.mobile_number
        employee_email_id = requested_employee_object.email_id
        employee_id = requested_employee_object.id

    return render_template('edit_employee.html', name=employee_name,
                           designation=employee_designation,
                           mobile_number=employee_mobile_number,
                           email_id=employee_email_id,
                           id=employee_id)


# This api will delete the existing employee
@app.route('/delete', methods=['POST'])  # http://127.0.0.1:5000/delete
def delete():
    get_request_data = request.values
    employee_id = get_request_data['id'][0]
    employee = Employee.query.get(employee_id)
    db.session.delete(employee)
    db.session.commit()

    # After deleting the record, show the home page
    all_data = Employee.query.all()  # Gives all data from Employee table
    return render_template('home.html', all_data=all_data)


if __name__ == '__main__':
    app.run(debug=True)
