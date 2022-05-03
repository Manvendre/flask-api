
from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy


app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:2083@localhost:5432/register'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

class Emp(db.Model):
    __tablename__='emps'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50),nullable=False)
    age = db.Column(db.Integer(),nullable=False) 
    password=db.Column(db.String(50),nullable=False)

    def __init__(self,name,age,password):
     self.name=name
     self.age=age
     self.password=password

db.create_all()

@app.route('/')
def welcome():

   
    return jsonify({"message":"hello employe"})

@app.route('/emp/<int:id>',methods=['GET'])
def emp(id):
    emp=Emp.query.get(id)
    del emp.__dict__['_sa_instance_state']
    return jsonify(emp.__dict__)

@app.route('/newemp',methods=['POST'])
def newemp():
    body=request.get_json()
    db.session.add(Emp(body['name'],body['age'],body['password']))
    db.session.commit()
    return jsonify({"message":"emp added"})

@app.route('/update/<int:id>',methods=['PUT'])
def update(id):
    body=request.get_json()
    db.session.query(Emp).filter_by(id=id).update(
    dict(name=body['name'], age=body['age'],password=body['password']))
    db.session.commit()
    return jsonify({"message":"emp updated"})

@app.route('/delete/<int:id>',methods=['DELETE'])
def delete(id):
    db.session.query(Emp).filter_by(id=id).delete()
    db.session.commit()
    return jsonify({"message":"emp deleted"})


if __name__== "__main__":
    app.run(debug=True)



