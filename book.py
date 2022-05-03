from flask import Blueprint, flash, render_template, request
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from forms import BookForm, SearchForm
from mydb import db
from models import Books
book = Blueprint('book',__name__, url_prefix='/book', static_folder='static')
from werkzeug.utils import secure_filename
import uuid as uuid
import os 
import app
#Add a book
@book.route('/book/add', methods=['GET','POST'])
@login_required
def add_book():
    name=None
    form=BookForm()
    if form.validate_on_submit():
        book = Books.query.filter_by(name=form.name.data).first()
        if book is None:
            book=Books(name=form.name.data, author=form.author.data, year_published=form.year_published.data, book_pic=form.book_pic.data)
            db.session.add(book)
            db.session.commit()
        name=form.name.data
        form.name.data=''
        form.author.data=''
        form.year_published.data=''
        form.book_pic.data=''
        flash("Book Added Successfully!")
    our_books=Books.query.order_by(Books.id)
    return render_template("add_book.html", form=form, name=name, our_books=our_books)


#update book database record
@book.route('/update_book/<int:id>', methods=['GET','POST'])
@login_required
def Update_book(id):
    form=BookForm()
    name_to_update=Books.query.get_or_404(id)
    if request.method=="POST":
        name_to_update.name=request.form['name']
        name_to_update.author=request.form['author']
        name_to_update.year_published=request.form['year_published']
        name_to_update.book_pic=request.files['book_pic']
        
        
        #grab image name
        book_filename = secure_filename(name_to_update.book_pic.filename)
        # set uuid
        pic_name = str(uuid.uuid1()) + "_" + book_filename
        #SAVE IMAGE
        name_to_update.book_pic.save(os.path.join(app.config['UPLOAD_FOLDER']), pic_name)
        #save to string to save in db
        name_to_update.book_pic = pic_name
        try:
            db.session.commit()
            flash('Book Updated Successfully!')
            return render_template("add_book.html", form=form, name_to_update=name_to_update, id=id)
        except:
            flash('Error! Try Again')
            return render_template ("update_book.html", form=form, name_to_update=name_to_update )
    else:
        return render_template ("update_book.html", form=form, name_to_update=name_to_update, id=id )

       
#Delete a book
@book.route('/delete_book/<int:id>')
@login_required
def delete_book(id):
    book_to_delete=Books.query.get_or_404(id)
    id = current_user.id
    if id == book_to_delete.orderer.id: 
        try:
            db.session.delete(book_to_delete)
            db.session.commit()
            flash('Book Deleted Successfully!')   
            our_books=Books.query.order_by(Books.id)
            return render_template("add_book.html", our_books=our_books)
        except:
            flash('Error! Try Again')
            our_books=Books.query.order_by(Books.id)
            return render_template("add_book.html", our_books=our_books)
    else:
            flash('Not Authorized To Delete This Book')
            our_books=Books.query.order_by(Books.id)
            return render_template("add_book.html", our_books=our_books)

   

