#Author: Mahmoud Hany
from flask import Flask,request,jsonify,make_response
from flask_sqlalchemy import SQLAlchemy
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)

    def __init__(self,username,password):
        self.username = username
        self.password = password
        
db.create_all()

#create a test route 
@app.route('/test',methods=['GET'])
def test():
    return make_response(jsonify({'message':'test route'}),200)

#create a user

@app.route('/users',methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        username = data['username']
        password = data['password']
        new_user = User(username,password)
        db.session.add(new_user)
        db.session.commit()
        return make_response(jsonify({'message':'User created'}),200)
    except Exception as e:
        print(e)
        return make_response(jsonify({'message':'User not created'}),500)
    
    #get all users
@app.route('/users',methods=['GET'])
def get_users():
    try:
        users=User.query.all()
        return make_response(jsonify([user.__dict__ for user in users]),200)
    except e:
        return make_response(jsonify({'message':'Error fetching users'}),500)
    
    #get a user by id 
    
    @app.route('/users/<id>',methods=['GET'])
    def get_user(id):
        try:
            user = User.query.filter_by(id=id).first()
            if user:
                return make_response(jsonify({'user',user.json}),200)
                return make_response(jsonify({'message':'User not found'}),404)
            return make_response(jsonify(user.__dict__),200)
        except Exception as e:
            return make_response(jsonify({'message':'Error fetching user'}),500)
        
    # update a user
    @app.route('/users/<id>',methods=['PUT'])
    def update_user(id):
        try:
            data = request.get_json()
            user = User.query.filter_by(id=id).first()
            user.username = data['username']
            user.password = data['password']
            db.session.commit()
            return make_response(jsonify({'message':'User updated'}),200)
            return make_response(jsonify({'message':'Error updating user'}),500)
            return make_response(jsonify({'message':'User updated'}),200)
        except e:
            return make_response(jsonify({'message':'Error updating user'}),500)    
        
    # delete a user
    @app.route('/users/<id>',methods=['DELETE'])
    def delete_user(id):
        try:
            user = User.query.filter_by(id=id).first()
            db.session.delete(user)
            db.session.commit()
            return make_response(jsonify({'message':'User deleted'}),200)
        except e:
            return make_response(jsonify({'message':'Error deleting user'}),500)    