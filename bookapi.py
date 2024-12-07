from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///booksdata.db'
db = SQLAlchemy(app)
api = Api(app)

class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(80), unique=True, nullable=False)
    author = db.Column(db.String(80), unique=True, nullable=False)
    publisher = db.Column(db.String(80), unique=True, nullable=False)
    
    def __repr__(self):
        return f"(book = {self.book_name}, author = {self.author}, publisher = {self.publisher})"

user_args = reqparse.RequestParser()
user_args.add_argument('book_name', type=str, required=True, help="Book Name cannot be blank")
user_args.add_argument('author', type=str, required=True, help="Email cannot be blank")
user_args.add_argument('publisher', type=str, required=True, help="Publisher cannot be blank")

userFields = {
    'id':fields.Integer,
    'book_name':fields.String,
    'author':fields.String,
    'publisher':fields.String,
}


class Users(Resource):
    @marshal_with(userFields)
    def get(self):
        users = UserModel.query.all()
        return users

    @marshal_with(userFields)
    def post(self):
        args = user_args.parse_args()
        user = UserModel(book_name=args["book_name"], author=args["author"], publisher=args["publisher"])
        db.session.add(user)
        db.session.commit()
        users = UserModel.query.all()
        return users, 201

class User(Resource):
    @marshal_with(userFields)
    def get(self, id):
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, "User not found")
        return user
    
    @marshal_with(userFields)
    def patch(self, id):
        args = user_args.parse_args()
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, "User not found")
        user.book_name = args["book_name"]
        user.author = args["author"]
        user.publisher = args["publisher"]
        db.session.commit()
        return user
    
    @marshal_with(userFields)
    def delete(self, id):
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, "User not found")
        db.session.delete(user)
        db.session.commit()
        users = UserModel.query.all()
        return users


api.add_resource(Users, '/api/users/')
api.add_resource(User, '/api/users/<int:id>')



@app.route('/')
def home():
    return '<h1>My Books API</h1>'


if __name__ == '__main__':
    app.run(debug=True)