from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DateField 
from wtforms.validators import DataRequired
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

#function to make customer name choice
def choice_query_customer():
    return Customers.query
def choice_query_book():
    return Books.query
class ChoiceForm(FlaskForm):
    customerid = QuerySelectField('Customer', query_factory=choice_query_customer, allow_blank=True,validators=[DataRequired()])
    bookid = QuerySelectField('Book', query_factory=choice_query_book, allow_blank=True,validators=[DataRequired()])
    issue_date = DateField('Issue Date',validators=[DataRequired()])
    return_date = DateField('Return date',validators=[DataRequired()])
    submit = SubmitField('Submit')