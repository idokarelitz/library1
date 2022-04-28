from flask import Blueprint, flash, render_template, request

from forms import BookForm, SearchForm
from mydb import db
from models import Books
book = Blueprint('book',__name__, url_prefix='/book')


#Add a book
@book.route('/book/add', methods=['GET','POST'])
def add_book():
    name=None
    form=BookForm()
    if form.validate_on_submit():
        book = Books.query.filter_by(name=form.name.data).first()
        if book is None:
            book=Books(name=form.name.data, author=form.author.data, year_published=form.year_published.data, book_type=form.book_type.data)
            db.session.add(book)
            db.session.commit()
        name=form.name.data
        form.name.data=''
        form.author.data=''
        form.year_published.data=''
        form.book_type.data=''
        flash("Book Added Successfully!")
    our_books=Books.query.order_by(Books.id)
    return render_template("add_book.html", form=form, name=name, our_books=our_books)


#update book database record
@book.route('/update_book/<int:id>', methods=['GET','POST'])
def Update_book(id):
    name=None
    form=BookForm()
    name_to_update=Books.query.get_or_404(id)
    if request.method=="POST":
        name_to_update.name=request.form['name']
        name_to_update.author=request.form['author']
        name_to_update.year_published=request.form['year_published']
        name_to_update.book_type=request.form['book_type']
        try:
            db.session.commit()
            form.name.data=''
            form.author.data=''
            form.year_published.data=''
            form.book_type.data=''
            flash('Book Updated Successfully!')
            our_books=Books.query.order_by(Books.id)
            return render_template("add_book.html", form=form, name=name, our_books=our_books)
        except:
            flash('Error! Try Again')
            return render_template ("update_book.html", form=form, name_to_update=name_to_update )
    else:
        return render_template ("update_book.html", form=form, name_to_update=name_to_update, id=id )
       
#Delete a book
@book.route('/delete_book/<int:id>')
def delete_book(id):
    book_to_delete=Books.query.get_or_404(id)
    name=None
    form=BookForm()  
    try:
        db.session.delete(book_to_delete)
        db.session.commit()
        flash('Book Deleted Successfully!')   
        our_books=Books.query.order_by(Books.id)
        return render_template("add_book.html", form=form, name=name, our_books=our_books)
    except:
        flash('Error! Try Again')
        return render_template("add_book.html", form=form, name=name, our_books=our_books)


