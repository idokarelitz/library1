from flask import Blueprint, flash, render_template, request

from forms import CustomerForm,Customer_Search_Form, IssueForm
from mydb import db
from models import Customers, Issue_book
customer = Blueprint('customer',__name__, url_prefix='/customer')




#Add a Customer
@customer.route('/customer/add', methods=['GET','POST'])
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
@customer.route('/update_customer/<int:id>', methods=['GET','POST'])
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
@customer.route('/delete/<int:id>')
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
    

@customer.route('/search_customer', methods=['GET','POST']) 
def search_customer():
    name=None
    form=Customer_Search_Form()
    if form.validate_on_submit():
        customer = Customers.query.filter_by(name=form.name.data)
        
        return render_template("search_customer.html", form=form, name=name, customer=customer)       
    else:
        return render_template("search_customer.html", form=form)       

