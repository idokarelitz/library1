from flask import Flask, render_template, flash
from datetime import timedelta
from mydb import db, migrate
from customer import customer
from book import book
from issue import issue
from forms import SearchForm, Search2Form, ChoiceForm
from models import Customers, Books, Issue_book
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
app.register_blueprint(issue)

#pass to nevbar
@app.context_processor
def base():
    form=SearchForm()
    return dict(form=form)
@app.context_processor
def base():
    form=Search2Form()
    return dict(form=form)

# Create search
@app.route('/search', methods=[ 'POST'])
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


@app.route('/order')
def order():
    form=ChoiceForm()
    if form.validate_on_submit():
        issue_book = Issue_book.query.filter_by(customer=form.customer.data).first()
        if issue_book is None:
            issue_book=Issue_book(customer=form.customer.data, book=form.book.data, issue_date=form.issue_date.data, return_date=form.return_date.data )
            db.session.add(issue_book)
            db.session.commit()
        
        flash("Issued book Successfully!")
    our_issues=Issue_book.query.order_by(Issue_book.id)
    return render_template("order.html", form=form, id=id, our_issues=our_issues)
    


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