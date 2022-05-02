# imports:

from wtforms.validators import DataRequired, EqualTo, Length

from wtforms import StringField, SubmitField, PasswordField, IntegerField, DateField, BooleanField, ValidationError 

from werkzeug.security import generate_password_hash, check_password_hash 

from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

1. in app.py -- class Users
---------------------------
# password hash
#make new column for password

    password_hash=db.Column(db.String(128))
    
# add property
# 1. message if somthing go wrong

    @property
    def password(self):
       raise AttributeError("password is not a readable attribute") 

# 2. set the password hash

    @password.setter
    def password(self, password):
        self.password_hash= generate_password_hash(password)

# 3. check if pass=hash

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

to check if working go terminal

1.flask shell
2.from app import Users  -- (flaskProject1)
3.u=Users()
4.u.password = 'select a password'
5.u.password  --  show error is good pass hashed
6.u.password_hash  -- show hash code
7.u.verify_password('selected password form before')--- True Fulse

add in app.py -- @app.route('/user/add'...

 # hash the password
            hashed_pw = generate_password_hash(form.password_hash.data, "sha256")
            user=Users(name=form.name.data, email=form.email.data, password_hash=hashed_pw)

            form.password_hash.data = ''

 #           -- UserForm:

password_hash = PasswordField('Password', validators=[DataRequired(), EqualTo('password_hash2', message='Passwords Must Match!')])

password_hash2 = PasswordField('Confirm Password', validators=[DataRequired()])

 # add_user.html

 {{ form.password_hash.label(class="form-label") }}

    {{ form.password_hash(class="form-control") }}
    <br />
    {{ form.password_hash2.label(class="form-label") }}

    {{ form.password_hash2(class="form-control") }}
    <br />

