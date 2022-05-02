
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DateField, PasswordField 
from wtforms.validators import DataRequired, EqualTo
from models import Customers, Books
from wtforms_sqlalchemy.fields import QuerySelectField

class SearchForm(FlaskForm):
    searched = StringField("Searched", validators=[DataRequired()])
    submit = SubmitField('Submit')
    
class Search2Form(FlaskForm):
    searched2 = StringField("Searched2", validators=[DataRequired()])
    submit = SubmitField('Submit')
#create a form class customer
class CustomerForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    username   = StringField('Username', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    age = StringField('Age', validators=[DataRequired()])
    email  = StringField('Email', validators=[DataRequired()])
    password_hash = PasswordField('Password', validators=[DataRequired(), EqualTo('password_hash2', message='Passwords Must Match!')])
    password_hash2 = PasswordField('Confirm Password', validators=[DataRequired()])
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

class OrderForm(FlaskForm):
    date_issued = DateField('Date Issued', validators=[DataRequired()])
    date_return = DateField('Date Return', validators=[DataRequired()])
    book_id = IntegerField('Book ID', validators=[DataRequired()])
    submit = SubmitField('Submit')
 
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")




#function to make customer name choice
def choice_query_customer():
    return Customers.query
def choice_query_book():
    return Books.query
class ChoiceForm(FlaskForm):
    customerid = QuerySelectField('Customer', query_factory=choice_query_customer, allow_blank=True,validators=[DataRequired()])
    bookid = QuerySelectField('Book', query_factory=choice_query_book, allow_blank=True,validators=[DataRequired()])
    submit = SubmitField('Submit')