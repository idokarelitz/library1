import datetime
from flask import Flask, render_template, flash, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DateField 
from wtforms.validators import DataRequired, EqualTo, Length
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from wtforms_sqlalchemy.fields import QuerySelectField

# Create a Flask Instance
app = Flask(__name__)


#add database sqlite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'




#create a secret key (csrf token)
app.config['SECRET_KEY'] = "vsdvlsdvdsldssdsdf"
#initialize the database
db= SQLAlchemy(app)
migrate=Migrate(app, db)



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
  
#create a form class customer
class CustomerForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    age = StringField('Age', validators=[DataRequired()])
    submit = SubmitField('Submit')

class Customer_Search_Form(FlaskForm):
    name = StringField('Name')
    city = StringField('City')
    age = StringField('Age')
    submit = SubmitField('Submit')
         
       

#create a form class book
class BookForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    year_published = StringField('Year Published', validators=[DataRequired()])
    book_type = StringField('book Type', validators=[DataRequired()])
    submit = SubmitField('Submit')
 
class IssueForm(FlaskForm):
    customerid = IntegerField('CustomerID',validators=[DataRequired()] )
    bookid = IntegerField('BookID',validators=[DataRequired()] )
    issue_date = DateField('Issue date')
    return_date = DateField('Return date')
    submit = SubmitField('Submit')

########################################################################
#                             CUSTOMERS                                #
########################################################################

@app.route('/search_customer', methods=['GET','POST']) 
def search_customer():
    name=None
    form=Customer_Search_Form()
    if form.validate_on_submit():
        customer = Customers.query.filter_by(name=form.name.data)
        
        return render_template("search_customer.html", form=form, name=name, customer=customer)       
    else:
        return render_template("search_customer.html", form=form)       

#issue a book
@app.route('/issue_book', methods=['GET','POST'])
def issue_book():
    id=None
    form=IssueForm()
    if form.validate_on_submit():
        issue_book = Issue_book.query.filter_by(customerid=form.customerid.data).first()
        if issue_book is None:
            issue_book=Issue_book(customerid=form.customerid.data, bookid=form.bookid.data, issue_date=form.issue_date.data, return_date=form.return_date.data)
            db.session.add(issue_book)
            db.session.commit()
        
        flash("Issued book Successfully!")
    our_issues=Issue_book.query.order_by(Issue_book.id)
    return render_template("issue_book.html", form=form, id=id, our_issues=our_issues)
    

 
#Add a Customer
@app.route('/customer/add', methods=['GET','POST'])
def add_customer():
    name=None
    form=CustomerForm()
    if form.validate_on_submit():
        customer = Customers.query.filter_by(name=form.name.data).first()
        if customer is None:
            customer=Customers(name=form.name.data, city=form.city.data, age=form.age.data)
            db.session.add(customer)
            db.session.commit()
        name=form.name.data
        form.name.data=''
        form.city.data=''
        form.age.data=''
        flash("Customer Added Successfully!")
    our_customers=Customers.query.order_by(Customers.date_added)
    return render_template("add_customer.html", form=form, name=name, our_customers=our_customers)


#update customer database record
@app.route('/update_customer/<int:id>', methods=['GET','POST'])
def Update_customer(id):
    name=None
    form=CustomerForm()
    name_to_update=Customers.query.get_or_404(id)
    if request.method=="POST":
        name_to_update.name=request.form['name']
        name_to_update.city=request.form['city']
        name_to_update.age=request.form['age']
        try:
            db.session.commit()
            form.name.data=''
            form.city.data=''
            form.age.data=''
            flash('Customer Updated Successfully!')
            our_customers=Customers.query.order_by(Customers.date_added)
            return render_template("add_customer.html", form=form, name=name, our_customers=our_customers)
        except:
            flash('Error! Try Again')
            return render_template ("update_customer.html", form=form, name_to_update=name_to_update )
    else:
        return render_template ("update_customer.html", form=form, name_to_update=name_to_update, id=id )
       
            
#Delete a Customer
@app.route('/delete/<int:id>')
def delete(id):
    customer_to_delete=Customers.query.get_or_404(id)
    name=None
    form=CustomerForm()  
    try:
        db.session.delete(customer_to_delete)
        db.session.commit()
        flash('Customer Deleted Successfully!')   
        our_customers=Customers.query.order_by(Customers.date_added)
        return render_template("add_customer.html", form=form, name=name, our_customers=our_customers)
    except:
        flash('Error! Try Again')
        return render_template("add_customer.html", form=form, name=name, our_customers=our_customers)
    
 
########################################################################
#                                 BOOKS                                #
########################################################################

 
 

    
#Add a book
@app.route('/book/add', methods=['GET','POST'])
def add_book():
    name=None
    form=BookForm()
    if form.validate_on_submit():
        book = Books.query.filter_by(name=form.name.data).first()
        if book is None:
            book=Books(name=form.name.data, author=form.author.data, year_published=form.year_published.data, book_type=form.book_type.data)
            db.session.add(book)
            db.session.commit()
        name=form.name.data
        form.name.data=''
        form.author.data=''
        form.year_published.data=''
        form.book_type.data=''
        flash("Book Added Successfully!")
    our_books=Books.query.order_by(Books.id)
    return render_template("add_book.html", form=form, name=name, our_books=our_books)


#update book database record
@app.route('/update_book/<int:id>', methods=['GET','POST'])
def Update_book(id):
    name=None
    form=BookForm()
    name_to_update=Books.query.get_or_404(id)
    if request.method=="POST":
        name_to_update.name=request.form['name']
        name_to_update.author=request.form['author']
        name_to_update.year_published=request.form['year_published']
        name_to_update.book_type=request.form['book_type']
        try:
            db.session.commit()
            form.name.data=''
            form.author.data=''
            form.year_published.data=''
            form.book_type.data=''
            flash('Book Updated Successfully!')
            our_books=Books.query.order_by(Books.id)
            return render_template("add_book.html", form=form, name=name, our_books=our_books)
        except:
            flash('Error! Try Again')
            return render_template ("update_book.html", form=form, name_to_update=name_to_update )
    else:
        return render_template ("update_book.html", form=form, name_to_update=name_to_update, id=id )
       
#Delete a book
@app.route('/delete_book/<int:id>')
def delete_book(id):
    book_to_delete=Books.query.get_or_404(id)
    name=None
    form=BookForm()  
    try:
        db.session.delete(book_to_delete)
        db.session.commit()
        flash('Book Deleted Successfully!')   
        our_books=Books.query.order_by(Books.id)
        return render_template("add_book.html", form=form, name=name, our_books=our_books)
    except:
        flash('Error! Try Again')
        return render_template("add_book.html", form=form, name=name, our_books=our_books)


   






########################################################################
#                                 ROUTES                               #
########################################################################
# Create a route decorator
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

# Create Custom Error Pages
# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
	return render_template("404.html"), 404

# Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
	return render_template("500.html"), 500

#start app
if __name__=='__main__':
    app.run(debug=True,port=9000)