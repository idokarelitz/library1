from flask import Flask, render_template, flash, redirect, url_for
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from werkzeug.security import check_password_hash 

from mydb import db, migrate
from customer import customer
from book import book
from forms import SearchForm, Search2Form, OrderForm, LoginForm
from models import Customers, Books, Orders
# Create a Flask Instance
app = Flask(__name__)
#add database sqlite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#create a secret key (csrf token)
app.config['SECRET_KEY'] = "vsdvlsdvdsldssdsdf"

db.init_app(app)
migrate.init_app(app, db)

app.register_blueprint(customer)
app.register_blueprint(book)

#flask login required
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_customer(customer_id):
    return Customers.query.get(int(customer_id))

#pass to nevbar
@app.context_processor
def base():
    form=SearchForm()
    return dict(form=form)
@app.context_processor
def base():
    form=Search2Form()
    return dict(form=form)


@app.route('/order', methods=['GET','POST'])
@login_required
def order():
    id=None
    form=OrderForm()
    
    if form.validate_on_submit():
        issue_book = Orders.query.filter_by(book=form.book_id.data).first()
        if issue_book is None:
            issued_by = current_user.id
            
            issue_book=Orders(issued_by=issued_by, date_issued=form.date_issued.data, date_return=form.date_return.data, book=form.book_id.data)
            db.session.add(issue_book)
            db.session.commit()
        
        flash("Issued book Successfully!")
    our_issues=Orders.query.order_by(Orders.date_issued)
    return render_template("order.html", form=form, id=id, our_issues=our_issues)
    

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

@app.route('/dashboard', methods=['GET','POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')

    


# Create search
@app.route('/search', methods=[ 'POST'])
@login_required
def search():
    form = SearchForm()
    customers=Customers.query
    if form.validate_on_submit():
        #get data from submitted form
        customer.searched=form.searched.data
        #query the db
        customers=customers.filter(Customers.name.like('%' + customer.searched + '%') | Customers.city.like('%' + customer.searched + '%'))
        #how i want to return data
        customers=customers.order_by(Customers.id).all()
        return render_template("search.html", form=form, searched=customer.searched, customers=customers)

# Create search
@app.route('/search_book', methods=[ 'POST'])
@login_required
def search_book():
    form = Search2Form()
    books=Books.query
    if form.validate_on_submit():
        #get data from submitted form
        book.searched2=form.searched2.data
        #query the db
        books=books.filter(Books.name.like('%' + book.searched2 + '%') | Books.author.like('%' + book.searched2 + '%'))
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