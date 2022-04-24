
from flask import Flask, render_template


#from wtforms_sqlalchemy.fields import QuerySelectField

from mydb import db, migrate
from customer import customer
from book import book
from issue import issue

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