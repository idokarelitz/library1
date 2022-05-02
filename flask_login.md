
pip install flask_login

login.html

dashboard.html


# for login - out button we use flask login to check if:

login - button on log out mode

logged out - button is on login mode

in navbar.html we use a if statment to check:

{% if current_user.is_authenticated %}
      <li class="nav-item">
        <a class="nav-link " href="{{ url_for('logout')}}">logout</a>
      </li>
      {% else %}
      <li class="nav-item">
        <a class="nav-link " href="{{ url_for('login')}}">login</a>
      </li>
      {% endif %}



# lock down pages for user logged in only use:

@login_required -- command to alow only logged in users to enter the page


#create login form
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    submit = SubmitField("submit")
