from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DateField 
from wtforms.validators import DataRequired


  
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

