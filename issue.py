from flask import Blueprint, flash, render_template, request

from forms import IssueForm
from mydb import db
from models import Issue_book

issue = Blueprint('issue',__name__, url_prefix='/issue')

#issue a book
@issue.route('/issue_book', methods=['GET','POST'])
def issue_book():
    id=None
    form=IssueForm()
    if form.validate_on_submit():
        issue_book = Issue_book.query.filter_by(customerid=form.customerid.data).first()
        if issue_book is None:
            issue_book=Issue_book(customerid=form.customerid.data, bookid=form.bookid.data, issue_date=form.issue_date.data, return_date=form.return_date.data)
            db.session.add(issue_book)
            db.session.commit()
        
        flash("Issued book Successfully!")
    our_issues=Issue_book.query.order_by(Issue_book.id)
    return render_template("issue_book.html", form=form, id=id, our_issues=our_issues)
    

  