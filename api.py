from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'crud.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), unique = True)
    email = db.Column(db.String(120), unique = True)

    def __init__(self, username, email):
        self.username = username
        self.email = email
    
    def json_output(self):
        return {'username' : self.username, 'email': self.email}

class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('username', 'email')
    
user_schema = UserSchema()
users_schema = UserSchema(many = True)

# Endpoint to create a new user
@app.route("/user", methods = ["POST"])
def add_user():
    content = request.get_json(force = True)
    print ("\nRequest data is ",content)
    username = content['username']
    email = content['email']
    new_user = User(username, email)

    db.session.add(new_user)
    db.session.commit()
    print("\n\nNEW USER CREATED IS ", new_user.json_output())
    return jsonify(new_user.json_output())

# endpoint to show all users
@app.route("/user", methods=["GET"])
def get_user():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result.data)

# endpoint to get detail by id
@app.route("/user/<id>", methods = ["GET"])
def user_detail(id):
    user = User.query.get(id)
    return user_schema.jsonify(user)

# endpoint to update user
@ app.route("/user/<id>", methods = ["PUT"])
def user_update(id):
    # Get the user by ID
    user = User.query.get(id)


    update_request = request.get_json(force = True)
    username = update_request['username']
    email = update_request['email']

    # Update content
    user.email = email
    user.username = username

    db.session.commit()
    return user_schema.jsonify(user)

# endpoint to delete user
@app.route("/user/<id>", methods=["DELETE"])
def user_delete(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return user_schema.jsonify(user)

if __name__ == '__main__':
    app.run(debug = True)