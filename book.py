from flask import Blueprint, flash, render_template
from flask_login import  login_required
from forms import BookForm
from mydb import db
from models import Books, Customers
book = Blueprint('book',__name__, url_prefix='/book', static_folder='static')




#book catalog
@book.route('/books', methods=['GET','POST'])
@login_required
def books():
    our_books=Books.query.order_by(Books.id)
    return render_template("books.html", our_books=our_books)

#Add a new book
@book.route('/book/add', methods=['GET','POST'])
@login_required
def add_book():
    name=None
    form=BookForm()
    if form.validate_on_submit():
        book = Books.query.filter_by(name=form.name.data).first()
        if book is None:
            book=Books(name=form.name.data, author=form.author.data, year_published=form.year_published.data, profile_pic=form.profile_pic.data)
            db.session.add(book)
            db.session.commit()
            name=form.name.data
            form.name.data=''
            form.author.data=''
            form.year_published.data=''
            form.profile_pic.data=''
            flash("Book Added Successfully! Book must have profile pic. please upload one.")
            
            id= book.id
            name_to_update=Books.query.get_or_404(id)
            return render_template ("update_book.html", form=form,name_to_update=name_to_update, id=id )
    
        else:
            flash('Error! Try Again')
            our_books=Books.query.order_by(Books.id)
            return render_template("add_book.html", form=form, our_books=our_books, name=name)
    our_books=Books.query.order_by(Books.id)
    return render_template("add_book.html", form=form, our_books=our_books, name=name)


       
#Delete a book
@book.route('/delete_book/<int:id>')
@login_required
def delete_book(id):
    book_to_delete=Books.query.get_or_404(id)
    name=None
    form=BookForm()  
    try:
        db.session.delete(book_to_delete)
        db.session.commit()
        flash('Book Deleted Successfully!')   
        our_books=Books.query.order_by(Books.id) 
        our_customers=Customers.query.order_by(Customers.date_added)
        return render_template("dashboard.html", form=form, our_books=our_books, our_customers=our_customers )
    except:
        flash('Error! Try Again')
        return render_template("add_book.html", form=form, name=name, our_books=our_books)

   

