from flask import Flask, render_template, request, flash, redirect, url_for
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from werkzeug.security import check_password_hash 
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
import uuid as uuid
import os 
#blueprint
from mydb import db, migrate
from customer import customer
from book import book
from forms import SearchForm, CustomerForm, BookForm, Search2Form, OrderForm, LoginForm
from models import Customers, Books, Orders
# Create a Flask Instance
app = Flask(__name__)
#add database sqlite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#create a secret key (csrf token)
app.config['SECRET_KEY'] = "vsdvlsdvdsldssdsdf"
#create route for image upload
UPLOAD_FOLDER = 'static/images/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db.init_app(app)
migrate.init_app(app, db)
#blueprints
app.register_blueprint(customer)
app.register_blueprint(book)

#flask login required
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
#login
@login_manager.user_loader
def load_customer(customer_id):
    return Customers.query.get(int(customer_id))

#pass to nevbar for search bar 
@app.context_processor
def base():
    form=SearchForm()
    return dict(form=form)
@app.context_processor
def base():
    form=Search2Form()
    return dict(form=form)

#admin route
@app.route('/admin', methods=['GET','POST'])
@login_required
def admin():
    id = current_user.id
    if id == 1:
        return render_template('admin.html')
    else:
        flash("Sorry You Must Be The Admin")
        return render_template('dashboard.html')



#update book database record
@app.route('/update_book/<int:id>', methods=['GET','POST'])
@login_required
def Update_book(id):
    form=BookForm()
    name_to_update=Books.query.get_or_404(id)
    if request.method=="POST":
        name_to_update.name=request.form['name']
        name_to_update.author=request.form['author']
        name_to_update.year_published=request.form['year_published']
        name_to_update.profile_pic=request.files['profile_pic']
        
        #grab image name
        pic_filename = secure_filename(name_to_update.profile_pic.filename)
        #set uuid
        pic_name = str(uuid.uuid1()) + "_" + pic_filename
        #save the image
        name_to_update.profile_pic.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name))
        #change to str to save to db
        name_to_update.profile_pic = pic_name
        try:
            db.session.commit()
            flash('Book Updated Successfully!')
            our_books=Books.query.order_by(Books.id) 
            our_customers=Customers.query.order_by(Customers.date_added)
            return render_template("dashboard.html", form=form, our_books=our_books, our_customers=our_customers )
        except:
            flash('Error! Try Again')
            return render_template ("update_book.html", form=form, name_to_update=name_to_update )
    else:
        return render_template ("update_book.html", form=form, name_to_update=name_to_update, id=id )


#update customer database record
@app.route('/update_customer/<int:id>', methods=['GET','POST'])
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
            our_books=Books.query.order_by(Books.id) 
            our_customers=Customers.query.order_by(Customers.date_added)
            return render_template("dashboard.html", form=form, our_books=our_books, our_customers=our_customers )

        except:
            flash('Error! Try Again')
            return render_template ("update_customer.html", form=form, name_to_update=name_to_update, id=id )
    else:
        return render_template ("update_customer.html", form=form, name_to_update=name_to_update, id=id )
          


#order route
@app.route('/order', methods=['GET','POST'])
@login_required
def order():
    id=None
    form=OrderForm()
    issue_book=None
    if form.validate_on_submit():
        issue_book = Orders.query.filter_by(book=form.book_id.data).first()
        if issue_book is None:
            type1=2
            type2=5
            type3=10
            issued_by = current_user.id
            date_issued=datetime.now()
            if form.days_return.data == type1:
                date_return=date_issued + \
                         timedelta(days = 2)
            elif form.days_return.data == type2:
                date_return=date_issued + \
                         timedelta(days = 5)
            elif form.days_return.data == type3:
                date_return=date_issued + \
                         timedelta(days = 10)
            else:
                flash("You Can Only Choose 2,5 or 10 Days!")
                our_books=Books.query.order_by(Books.id)
                our_issues=Orders.query.order_by(Orders.date_issued)
                return render_template("order.html", form=form, id=id, our_issues=our_issues, our_books=our_books)
            issue_book=Orders(issued_by=issued_by, date_issued=date_issued, date_return=date_return, book=form.book_id.data)
            db.session.add(issue_book)
            db.session.commit()
        else:
            flash("Book Already Issued!")
            our_books=Books.query.order_by(Books.id)
            our_issues=Orders.query.order_by(Orders.date_issued)
            return render_template("order.html", form=form, id=id, our_issues=our_issues, our_books=our_books)
        days_return=form.days_return.data
        form.days_return.data=''
        form.book_id.data=''
        flash("Issued book Successfully!")
        our_books=Books.query.order_by(Books.id)
        our_issues=Orders.query.order_by(Orders.date_issued)
        return render_template("order.html", form=form, id=id, our_issues=our_issues, our_books=our_books)
    our_books=Books.query.order_by(Books.id)
    our_issues=Orders.query.order_by(Orders.date_issued)
    return render_template("order.html", form=form, id=id, our_issues=our_issues, our_books=our_books)
    
#Delete a order RETURN  
@app.route('/delete_order/<int:id>')

def delete_order(id):
    order_to_delete=Orders.query.get_or_404(id)
    name=None
    form=OrderForm()  
    try:
        db.session.delete(order_to_delete)
        db.session.commit()
        flash('Order Returned Successfully!')   
        our_orders=Orders.query.order_by(Orders.date_issued)
        our_books=Books.query.order_by(Books.id)
        return render_template("order.html", form=form, name=name, our_orders=our_orders,our_books=our_books)
    except:
        flash('Error! Try Again')
        our_orders=Orders.query.order_by(Orders.date_issued)
        return render_template("order.html", form=form, name=name, our_orders=our_orders)
    
    
    

#create login page
@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        customer = Customers.query.filter_by(username=form.username.data).first()
        if customer:
            #check the hash
            if check_password_hash(customer.password_hash, form.password.data):
                login_user(customer)
                
                return redirect(url_for('dashboard'))
            else:
                flash("Wrong Password - Try Again")    
        else:
            flash("That Customer Doesn't Exist")
    return render_template('login.html', form=form)

#create logout function
@app.route('/logout', methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    flash("You Have Been Logged Out")
    return redirect(url_for('login'))

#dashboard route
@app.route('/dashboard', methods=['GET','POST'])
@login_required
def dashboard():
    our_books=Books.query.order_by(Books.id) 
    our_customers=Customers.query.order_by(Customers.date_added)
    our_issues=Orders.query.order_by(Orders.date_issued)
    return render_template('dashboard.html', our_books=our_books, our_customers=our_customers,our_issues=our_issues)

# Create search customer
@app.route('/search', methods=[ 'POST'])
@login_required
def search():
    form = SearchForm()
    customers=Customers.query
    if form.validate_on_submit():
        #get data from submitted form
        customer.searched=form.searched.data
        #query the db
        customers=customers.filter(Customers.name.like('%' + customer.searched + '%'))
        #how i want to return data
        customers=customers.order_by(Customers.id).all()
        return render_template("search.html", form=form, searched=customer.searched, customers=customers)
    
# Create search book
@app.route('/search_book', methods=[ 'GET','POST'])
@login_required
def search_book():
    form = Search2Form()
    books=Books.query
    if form.validate_on_submit():
        #get data from submitted form
        book.searched2=form.searched2.data
        #query the db
        books=books.filter(Books.name.like('%' + book.searched2 + '%'))
        #how i want to return data
        books=books.order_by(Books.id).all()
        return render_template("search_book.html", form=form, searched2=book.searched2, books=books)


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