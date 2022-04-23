---------------
1. VIRTUAL ENV:
---------------
    1. py -m venv env

    2. Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

    3. cd env/scripts

    4. activate.ps1


---------
2.  PIP:
---------
    pip install Flask
    pip install python-dotenv
    pip install -U Flask-SQLAlchemy
    pip install Flask-WTF
    pip install wtforms-widgets
    pip install Flask-Migrate
    pip install WTForms-SQLAlchemy


--------------
3. .gitignore:
--------------
 #  Put the env in your .gitignore:
    
    git init
    
    echo 'venv' > .gitignore 

 #  Activate the environment
    
    
 #  Install all pips

 #  Freeze the requirements:

    pip freeze > requirements.txt

 # Check requirements.txt into source control:

    git add requirements.txt


-----------------
4. GIT -- GITHUB:
-----------------

SAVE A PROJECT TO GIT -- open BASH TERMINAL:
--------------------------------------------


1. git config --global user.name "Ido Karelitz"

2. git config --global user.email "idoinfo@gmail.com"

3. git config --global push.default matching

4. git config --global alias.co checkout

5. git init

6. git add .

7. git commit -am "Initial Commit"

8. cd ..

9. cd ~/

10. mkdir .ssh

11. cd .ssh

12. ssh-keygen.exe

13. enter  -- will save in local dir

14. enter  -- will skip password create don't need
    enter

15. made a ssh key to check do -- ls

16. you need the pub file for github

cat id_rsa.pub

    copy the code (without cat id_ras.pub)

NOW OPEN GITHUB
---------------
1. in small icon on top right - go to settings

2. ssh and gpg keys

3. add new ssh

4. name

5. past ssh key

6.add

7. back to repositories

8. new - name - create

#navigate back to project dir

9. do all commands on push section (in github page)

UPDATE GITHUB PROJECT
---------------------

1.git add .

2. git commit -am 'small description of changes'

3. git push

4. will identify and update only changed files


--------------------
5. FLASK-SQLALCHEMY:
--------------------
# MAKE NEW DATABASE
-------------------
  terminal: 1.python
            2.from app import db
            3.db.create_all()
            4.exit()

app.py
------
from flask_sqlalchemy import SQLAlchemy
import datetime


#add database sqlite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

#create a secret key (csrf token)
app.config['SECRET_KEY'] = "idokar"

#initialize the database
db= SQLAlchemy(app)

#create model EXAMPLE:
class Users(db.Model):
    id         = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(200), nullable=False)
    email      = db.Column(db.String(120), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.datetime.utcnow)

-----------------
6. FLASK-MIGRATE:
-----------------
# TO UPDATE A TABLE IN THE DB:
------------------------------
1. add column in all pages:
        app.py:
            1. from flask_migrate import Migrate
            2.UserForm
            3.routes: update, add
        update info in:    
            1.update.html
            2.add_user.html

        UNDER: db= SQLAlchemy(app)
        WRITE: migrate=Migrate(app, db)

2.terminal:

    1.flask db init  --> makes new dir migrate
    2.flask db  --> to see options
    3.flask db migrate -m 'Initial Migration' -->temp db file
    4.flask db upgrade  --> push new db

    to make new changes :

    1.flask db migrate -m "added something"
    2.flask db upgrade


-----------
7. WTFORMS:
-----------
functions to use in wtforms
---------------------------
## fields
    # BooleanField
	# DateField
	# DateTimeField
	# DecimalField
	# FileField
	# HiddenField
	# MultipleField
	# FieldList
	# FloatField
	# FormField
	# IntegerField
	# PasswordField
	# RadioField
	# SelectField
	# SelectMultipleField
	# SubmitField
	# StringField
	# TextAreaField

## Validators
	# DataRequired
	# Email
	# EqualTo
	# InputRequired
	# IPAddress
	# Length
	# MacAddress
	# NumberRange
	# Optional
	# Regexp
	# URL
	# UUID
	# AnyOf
	# NoneOf






GIT BASH TERMINAL:
-----------------

pwd - show location in file
ls - show in file
cd - go in...
cd .. - go out...
c: d: - hdd select
clear - clear screen
mkdir - make new directory
mkdir .name - make unseen directory