from flask import Flask,  request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

main = Flask(__name__)

path = Api(main)

main.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@34.172.206.228/empdata'
main.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(main)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    technology = db.Column(db.String(40), nullable=False)
    gender = db.Column(db.String(40), nullable=False)

    def __repr__(self):
        return f"{self.name} - {self.technology} - {self.gender} - {self.id}"



class Get(Resource):
    def get(self):
        empls = Employee.query.all()
        list = []
        for emp in empls:
            data = {'Emp_Id': emp.id, 'Name': emp.name, 'Technology': emp.technology, 'Gender': emp.gender}
            list.append(data)
        return {"Employees": list}

class GetById(Resource):
    def get(self, id):
        emp = Employee.query.get(id)
        if emp is None:
            return {'error': 'not found'}
        else:
            data = {'Emp_Id': emp.id, 'Name': emp.name, 'Technology': emp.technology, 'Gender': emp.gender}

            return {"Employee": data}
                


class Create(Resource):
    def post(self):
        if request.is_json:
            emp = Employee(id=request.json['Emp_Id'],name=request.json['Name'], technology=request.json['Technology'],
                       gender=request.json['Gender'])
            db.session.add(emp)
            db.session.commit()
            return 'Created.'
        else:
            return {'error': 'Request must be JSON'}


class Update(Resource):
    def put(self, id):
        if request.is_json:
            emp = Employee.query.get(id)
            if emp is None:
                return {'error': 'not found'}
            else:
                emp.name = request.json['Name']
                emp.technology = request.json['Technology']
                emp.gender = request.json['Gender']
                db.session.commit()
                return 'Updated.'
        else:
            return {'error': 'Request must be JSON'}


class Delete(Resource):
    def delete(self, id):
        emp = Employee.query.get(id)
        if emp is None:
            return {'error': 'not found'}
        db.session.delete(emp)
        db.session.commit()
        return f'deleted'


path.add_resource(Get, '/employee')
path.add_resource(GetById, '/employee/<int:id>')
path.add_resource(Create, '/create')
path.add_resource(Update, '/update/<int:id>')
path.add_resource(Delete, '/delete/<int:id>')


if __name__ == '__main__':
    main.run(debug=True)
