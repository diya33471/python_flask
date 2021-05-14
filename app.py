from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5433/postgres"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



class StudentModel(db.Model):
    __tablename__ = 'students'

    roll = db.Column(db.String(), primary_key=True)
    name = db.Column(db.String())
    city = db.Column(db.String())
    country = db.Column(db.Integer())

    def __init__(self, name, city, country,roll):
        self.roll=roll
        self.name = name
        self.city = city
        self.country = country

    def __repr__(self):
        return f"<Student {self.name}>"


@app.route('/')
def hello():
	return {"hello": "world"}


@app.route('/students', methods=['POST', 'GET'])
def handle_cars():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_student = StudentModel(name=data['name'], city=data['city'],roll=data['roll'], country=data['country'])

            db.session.add(new_student)
            db.session.commit()

            return {"message": f"Student {new_student.name} has been created successfully."}
        else:
            return {"error": "The request payload is not in JSON format"}

    elif request.method == 'GET':
        students = StudentModel.query.all()
        print(students)
        results = [
            {
                "name": student.name,
                "city": student.city,
                "country": student.country,
                "roll" : student.roll
            } for student in students]

        return {"count": len(results), "Students": results, "message": "success"}


@app.route('/student/<student_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_student(student_id):
    student = StudentModel.query.get_or_404(student_id)

    if request.method == 'GET':
        response = {
            "name": student.name,
            "roll": student.roll,
            "city": student.city,
            "country": student.country
        }
        return {"message": "success", "student": response}

    elif request.method == 'PUT':
        data = request.get_json()
        student.name = data['name']
        student.roll = data['roll']
        student.city = data['city']
        student.country = data['country']

        db.session.add(student)
        db.session.commit()
        
        return {"message": f"student {student.name} successfully updated"}

    elif request.method == 'DELETE':
        db.session.delete(student)
        db.session.commit()
        
        return {"message": f"student {student.name} successfully deleted."}


if __name__ == '__main__':
    app.run(debug=True)