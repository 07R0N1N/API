from flask import Flask , request , jsonify
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///customers.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Customer(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    name = db.Column(db.String(100) , nullable = True)
    age = db.Column(db.Integer , nullable = True)
    number = db.Column(db.Integer , nullable = True)
    email = db.Column(db.String(100) , nullable = True)

# TO DISPLAY THE ENTIRE DATABASE TABLE
# def result():
#     customers = Customer.query.all()
#     customer_list = [
#         {
#         'id' : customer.id,
#         'name' : customer.name,
#         'age' : customer.age,
#         'number' : customer.number,
#         'email' : customer.email
#     }        
#     for customer in customers
#     ]
#     return customer_list

#TO INPUT DATA INTO THE TABLE
@app.route("/post_customer/" , methods = ['POST'])
def add_customer():
    try:
        data = request.get_json()
        new_customer = Customer(**data)
        db.session.add(new_customer) 
        db.session.commit()
        customers = Customer.query.all()
        customer_list = [
            {
            'id' : customer.id,
            'name' : customer.name,
            'age' : customer.age,
            'number' : customer.number,
            'email' : customer.email
        }        
        for customer in customers
        ]
        return jsonify({"message" : "Customer added Successfully" , "customers" : customer_list }) , 201
    
    except Exception as e:
        return jsonify({"error" : str(e) , "cpde" : 500}) 


@app.route("/get_customer/" , methods = ['GET'])
def get_customer():
    
    try:
        data = request.get_json()
        id = data.get("id")
        name = data.get("name")
        email = data.get("email")
        number = data.get("number")
        age = data.get("age")
        if id:
            customer = Customer.query.filter_by(id=id).all()
        elif name:
            customer = Customer.query.filter_by(name=name).all()
        elif age:
            customer = Customer.query.filter_by(age=age).all()
        elif number:
            customer = Customer.query.filter_by(number).all()
        elif email:
            customer = Customer.query.filter_by(email).all()
        else:
                return jsonify({}) , 200

        if customer:
                customer_list = [{
                    "id" : customers.id,
                    "name" : customers.name,
                    "age" : customers.age,
                    "phone_number" : customers.number,
                    "email" : customers.email
                }
                for customers in customer
                ]
                return jsonify({ "message" : "Found the Customers" , "customers" : customer_list})
        else:
                return jsonify({}) , 200
        
    except Exception as e:
        return jsonify({"error" : str(e) , "code" : 500})

@app.route("/put_customer" , methods = ['PUT'])
def update_customer():
    try:
        data = request.get_json()
        id = data.get("id")
        customer = Customer.query.get(id)

        if not customer:
            return jsonify({})

        for key , value in data.items():
            setattr( customer , key , value)

        db.session.commit()
        return jsonify({"message" : "Customer updated Successfully"}) , 200

    except Exception as e:
        return jsonify({"error" : str(e) , "code" : 500})       
#STARTING TEST TOUTORIAL  
# @app.route("/get-user/<user_data>")
# def home(user_data):
#     data = {
#         "id" : "name",
#         "date" : user_data,
#         "age" : "5"
#     }

#     extra = request.args.get("extra")
#     if extra:
#         data["extra"] = extra
#     return jsonify(data) , 200

# @app.route("/create-user/" , methods = ["POST"])
# def create_user():
#     data = request.get_json()

#     return jsonify(data) , 201


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)