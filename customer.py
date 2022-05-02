from flask import Blueprint, flash, render_template, request
from werkzeug.security import generate_password_hash
from flask_login import login_user, LoginManager, login_required, logout_user, current_user

from forms import CustomerForm
from mydb import db
from models import Customers
customer = Blueprint('customer',__name__, url_prefix='/customer')



@customer.route('/customers', methods=['GET','POST'])
@login_required
def customers():
    name=None
    form=CustomerForm()
    if form.validate_on_submit():
        customer = Customers.query.filter_by(name=form.name.data).first()
        if customer is None:
            #hash the password
            hashed_pw = generate_password_hash(form.password_hash.data, "sha256")
            customer=Customers(username=form.username.data, name=form.name.data, city=form.city.data, age=form.age.data, email=form.email.data, password_hash=hashed_pw)
            db.session.add(customer)
            db.session.commit()
        name=form.name.data
        form.name.data=''
        form.username.data=''
        form.city.data=''
        form.age.data=''
        form.email.data=''
        form.password_hash.data = ''
        flash("Customer Added Successfully!")
    our_customers=Customers.query.order_by(Customers.date_added)
    return render_template("customers.html", form=form, name=name, our_customers=our_customers)



 
#Add a Customer
@customer.route('/register_new', methods=['GET','POST'])
def register_new():
    name=None
    form=CustomerForm()
    if form.validate_on_submit():
        customer = Customers.query.filter_by(name=form.name.data).first()
        if customer is None:
            #hash the password
            hashed_pw = generate_password_hash(form.password_hash.data, "sha256")
            customer=Customers(username=form.username.data, name=form.name.data, city=form.city.data, age=form.age.data, email=form.email.data, password_hash=hashed_pw)
            db.session.add(customer)
            db.session.commit()
        name=form.name.data
        form.name.data=''
        form.username.data=''
        form.city.data=''
        form.age.data=''
        form.email.data=''
        form.password_hash.data = ''
        flash("Customer Added Successfully!")
    our_customers=Customers.query.order_by(Customers.date_added)
    return render_template("register_new.html", form=form, name=name, our_customers=our_customers)


#update customer database record
@customer.route('/update_customer/<int:id>', methods=['GET','POST'])
@login_required
def Update_customer(id):
    form=CustomerForm()
    name_to_update=Customers.query.get_or_404(id)
    if request.method=="POST":
        name_to_update.name=request.form['name']
        name_to_update.username=request.form['username']
        name_to_update.city=request.form['city']
        name_to_update.age=request.form['age']
        name_to_update.email=request.form['email']
        try:
            db.session.commit()
            flash('Customer Updated Successfully!')
            return render_template("update_customer.html", form=form, name_to_update=name_to_update, id=id)
        except:
            flash('Error! Try Again')
            return render_template ("update_customer.html", form=form, name_to_update=name_to_update, id=id )
    else:
        return render_template ("update_customer.html", form=form, name_to_update=name_to_update, id=id )
       
            
#Delete a Customer
@customer.route('/delete/<int:id>')
@login_required
def delete_customer(id):
    customer_to_delete=Customers.query.get_or_404(id)
    id = current_user.id
    if id == customer_to_delete.issuer.id: 
        try:
            db.session.delete(customer_to_delete)
            db.session.commit()
            flash('customer Deleted Successfully!')   
            our_customers=Customers.query.order_by(Customers.id)
            return render_template("add_customer.html", our_customers=our_customers)
        except:
            flash('Error! Try Again')
            our_customers=Customers.query.order_by(Customers.id)
            return render_template("add_customer.html", our_customers=our_customers)
    else:
            flash('Not Authorized To Delete This customer')
            our_customers=Customers.query.order_by(Customers.id)
            return render_template("add_customer.html", our_customers=our_customers)

    
 
