import datetime
from werkzeug.security import generate_password_hash, check_password_hash 
from mydb import db
from flask_login import UserMixin

#create model for customers
class Customers(db.Model, UserMixin):
    id        = db.Column(db.Integer, primary_key=True)
    name      = db.Column(db.String(200), nullable=False)
    username   = db.Column(db.String(20), nullable=False, unique=True)
    city      = db.Column(db.String(200), nullable=False)
    age       = db.Column(db.String(10), nullable=False)
    email      = db.Column(db.String(120), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    issue_book = db.relationship("Orders", backref="issuer", lazy=True)
    #password hash
    password_hash= db.Column(db.String(128))
    #add property
    #1. message if somthing go wrong
    @property
    def password(self):
       raise AttributeError("password is not a readable attribute") 
    #2. set the password hash
    @password.setter
    def password(self, password):
        self.password_hash= generate_password_hash(password)
    #3. check if pass=hash
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
        
    def __repr__(self):
        return '<Name %r>' % self.name


#create model for books
class Books(db.Model):
    id             = db.Column(db.Integer, primary_key=True)
    name           = db.Column(db.String(200), nullable=False, unique=True)
    author         = db.Column(db.String(200), nullable=False)
    year_published = db.Column(db.Integer, nullable=False)
    book_type      = db.Column(db.Integer, nullable=False)
    copy = db.relationship("Orders", backref="orderer", lazy=True)
    
    
    def __repr__(self):
        return '<Name %r>' % self.name

class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    issued_by = db.Column(db.Integer, db.ForeignKey("customers.id"))
    date_issued = db.Column(db.DateTime(), default=None)
    date_return = db.Column(db.DateTime(), default=None)
    book = db.Column(db.Integer, db.ForeignKey("books.id"))


  


