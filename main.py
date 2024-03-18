from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import json

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:''@localhost/emp_management'

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)   
    name = db.Column(db.String(80), unique=True)
    def __init__(self, name):
        self.name = name    

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    title = db.Column(db.String(80))
    department = db.Column(db.String(80))

    def __init__(self, name, title, department,department_id):
        self.name = name,
        self.title = title,
        self.department_id = department_id,
        self.department = department


with app.app_context():
    db.create_all()    

@app.route('/')
def index():
    
    return 'Hello'

#creating department rows
@app.route('/createDepartment')
def CreateDepartment(): #Change department otherwise it will throw error for duplicate entry
    with app.app_context():
        dept = Department(name='PHP')
        db.session.add(dept)
        db.session.commit()   
    return 'Succes'        

#Department data into json file
@app.route('/fetchDeptData')
def fetchDeptData():
    with app.app_context():
        datas = Department.query.all()
        print('data is',datas)
        result = [{'id':data.id,'name':data.name} for data in datas]
        with open('fetchDeptData.json','w') as f:
            json.dump(jsonify(result).json, f)
    return jsonify(result)

#update deparment table rows using id
@app.route('/UpdateDepartment/<int:id>')
def UpdateDepartment(id): #Change department otherwise it will throw error for duplicate entry
    with app.app_context():
        dept = Department.query.get(id)
        name = "Java"
        if name:
            dept.name = name
            db.session.commit()   
    return 'Updated Successfully'        

#create employee data
@app.route('/createEmployee')
def CreateEmployee():
    with app.app_context():
        emp = Employee(name='Rishabh Kumar', department_id=1, title='Software Developer', department='Python')
        db.session.add(emp)
        db.session.commit()   
    return 'Succes'        



#dump employee data into json file
@app.route('/fetchAllEmpData')
def fetchAllEmpData():
    with app.app_context():
        datas = Employee.query.all()
        print('data is',datas)
        result = [{'id':data.id,'name':data.name,'title':data.title,'department':data.department} for data in datas]
        with open('EmployeeData.json','w') as f:
            json.dump(jsonify(result).json, f)
    return jsonify(result)

#update employee field as per requirement
@app.route('/UpdateEmployee/<int:id>')
def UpdateEmployee(id):
    # print(id)
    with app.app_context():
        data = Employee.query.get(id)
        if data==None:
            print("Data is none")
            return 'No data found for delete'        
        elif data!=None:
            name = "Rishabh Kumar"
            title = "Web Developer"
            department = "PHP"
            if name:
                data.name = name
            if title:
                data.title = title
            if department:
                data.department = department
            
            db.session.commit()
        return 'Updated Successfully'        


#delete employe row using id

@app.route('/deleteEmployee/<int:id>')
def deleteEmployee(id):
    print(id)
    with app.app_context():
        data = Employee.query.get(id)
        if data==None:
            print("Data is none")
            return 'No data found for delete'        
        elif data!=None:
            db.session.delete(data)
            db.session.commit()
        return 'Deleted Successfully'        


if __name__=='__main__':
    app.run(debug = True)
