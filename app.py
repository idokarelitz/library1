import datetime
from flask import Flask, render_template, flash, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField 
from wtforms.validators import DataRequired, EqualTo, Length
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


# Create a Flask Instance
app = Flask(__name__)


#add database sqlite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///customers.db'

app.config['SQLALCHEMY_BINDS'] = { 'books' : 'sqlite:///books.db' }


#create a secret key (csrf token)
app.config['SECRET_KEY'] = "idokar"
#initialize the database
db= SQLAlchemy(app)
migrate=Migrate(app, db)

########################################################################
#                             CUSTOMERS                                #
########################################################################

#create model for customers
class Customers(db.Model):
    id        = db.Column(db.Integer, primary_key=True)
    name      = db.Column(db.String(200), nullable=False, unique=True)
    city      = db.Column(db.String(200), nullable=False)
    age       = db.Column(db.String(10), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
#create a string for model customers
    def __repr__(self):
        return '<Name %r>' % self.name


#create a form class customer
class CustomerForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    age = StringField('Age', validators=[DataRequired()])
    submit = SubmitField('Submit')
    
 
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
#create model for books
class Books(db.Model):
    __bind_key__ = 'books'
    id             = db.Column(db.Integer, primary_key=True)
    name           = db.Column(db.String(200), nullable=False, unique=True)
    author         = db.Column(db.String(200), nullable=False)
    year_published = db.Column(db.Integer, nullable=False)
    book_type      = db.Column(db.Integer, nullable=False)
    date_added     = db.Column(db.DateTime, default=datetime.datetime.utcnow)
 
 
#create a form class book
class BookForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    year_published = StringField('Year Published', validators=[DataRequired()])
    book_type = StringField('book Type', validators=[DataRequired()])
    submit = SubmitField('Submit')
 
    
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
    our_books=Books.query.order_by(Books.date_added)
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
            our_books=Books.query.order_by(Books.date_added)
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
        our_books=Books.query.order_by(Books.date_added)
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