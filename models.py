import datetime
from mydb import db


#create model for customers
class Customers(db.Model):
    id        = db.Column(db.Integer, primary_key=True)
    name      = db.Column(db.String(200), nullable=False, unique=True)
    city      = db.Column(db.String(200), nullable=False)
    age       = db.Column(db.String(10), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    cus_book = db.relationship("Issue_book", backref="issue", lazy=True)
    
    def __repr__(self):
        return '<Name %r>' % self.name


#create model for books
class Books(db.Model):
    id             = db.Column(db.Integer, primary_key=True)
    name           = db.Column(db.String(200), nullable=False, unique=True)
    author         = db.Column(db.String(200), nullable=False)
    year_published = db.Column(db.Integer, nullable=False)
    book_type      = db.Column(db.Integer, nullable=False)
    issue_book = db.relationship(
        "Issue_book", backref=db.backref("loan", lazy=True))
    
  
class Issue_book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customerid = db.Column(db.Integer, db.ForeignKey("customers.id"), nullable=True, default=None)
    bookid = db.Column(db.Integer, db.ForeignKey("books.id"))
    issue_date = db.Column(db.DateTime())
    return_date = db.Column(db.DateTime())

