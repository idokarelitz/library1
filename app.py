import datetime
from flask import Flask, render_template, flash, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField 
from wtforms.validators import DataRequired, EqualTo, Length
from flask_sqlalchemy import SQLAlchemy



# Create a Flask Instance
app = Flask(__name__)


#add database sqlite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///customers.db'
#create a secret key (csrf token)
app.config['SECRET_KEY'] = "idokar"
#initialize the database
db= SQLAlchemy(app)


#create model
class Customers(db.Model):
    id        = db.Column(db.Integer, primary_key=True)
    name      = db.Column(db.String(200), nullable=False, unique=True)
    city      = db.Column(db.String(200), nullable=False)
    age       = db.Column(db.String(10), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
#create a string for model
    def __repr__(self):
        return '<Name %r>' % self.name

#create a form class
class CustomerForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    city = StringField('city', validators=[DataRequired()])
    age = StringField('age', validators=[DataRequired()])
    submit = SubmitField('submit')
    
 
 
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


#update database record
@app.route('/update/<int:id>', methods=['GET','POST'])
def Update(id):
    form=CustomerForm()
    name_to_update=Customers.query.get_or_404(id)
    if request.method=="POST":
        name_to_update.name=request.form['name']
        name_to_update.city=request.form['city']
        name_to_update.age=request.form['age']
        try:
            db.session.commit()
            flash('Customer Updated Successfully!')
            return render_template ("update.html", form=form, name_to_update=name_to_update, id=id )
        except:
            flash('Error! Try Again')
            return render_template ("update.html", form=form, name_to_update=name_to_update )
    else:
        return render_template ("update.html", form=form, name_to_update=name_to_update, id=id )
            


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