from flask import Blueprint, render_template, redirect, url_for, session, flash
from functools import wraps
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from password_validator import PasswordValidator

import podcast.adapters.repository as repo
import podcast.authentication.services as services

auth_blueprint = Blueprint('auth_bp', __name__, url_prefix='/authentication')


@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    exception_message = None

    # if form.is_submitted():
    #     print("Form submitted")
    #
    # if form.validate():
    #     print("Form is valid")
    #     try:
    #         services.add_user(form.username.data, form.password.data, repo.repo_instance)
    #         return redirect(url_for('auth_bp.login'))
    #     except services.NameNotUniqueException:
    #         exception_message = "Username is already taken"
    # else:
    #     print("Form is not valid")
    #     print(f"Form errors: {form.errors}")

    if form.validate_on_submit():
        try:
            services.add_user(form.username.data.lower(), form.password.data, repo.repo_instance)
            return redirect(url_for('auth_bp.login'))

        except services.NameNotUniqueException:
            exception_message = "Username is already taken"

    else:
        print(f"Form errors: {form.errors}")

    return render_template("authentication/auth.html",
                           title="Register",
                           form=form,
                           user_message=exception_message,
                           password_message=None,
                           handler_url=url_for('auth_bp.register')
                           )


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    unregistered = None
    unmatch_password_username = None

    if form.validate_on_submit():
        try:
            user = services.get_user(form.username.data.lower(), form.password.data, repo.repo_instance)
            services.auth_user(user['username'], form.password.data, repo.repo_instance)

            session.clear()
            # print("session does not exist", session is None)
            session['username'] = user['username']
            # print("session: ", session.values())

            # response = redirect(url_for('home_bp.home'))

            print("success login")
            print(session['username'])

            return redirect(url_for('auth_bp.redirect_login'))


        except services.UnregisteredUserException:
            unregistered = "Username not recognised/not registered"

        except services.UnauthenticatedUserException:
            unmatch_password_username = "Username and password do not match"



    return render_template("authentication/auth.html",
                           title="Login",
                           form=form,
                           user_message=unregistered,
                           password_message=unmatch_password_username,
                           handler_url=url_for('auth_bp.login')
                           )



@auth_blueprint.route('/logout')
def logout():
    session.clear()
    print("session has been cleared")
    return redirect(url_for('auth_bp.redirect_logout'))

def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        print("check login requirement:", session.get('username'))
        if not session.get('username'):
            return redirect(url_for('auth_bp.login'))
        return view(**kwargs)
    return wrapped_view

@auth_blueprint.route('/redirect_login')
def redirect_login():
    return render_template('authentication/redirect_login.html')

@auth_blueprint.route('/redirect_logout')
def redirect_logout():
    return render_template('authentication/redirect_logout.html')

# class UsernameValid:
#     def __init__(self, message=None):
#         if not message:
#             message = "Username is already taken"
#         self.message = message
#
#     def __call__(self, form, field):
#         if field.data ==


class PasswordValid:
    def __init__(self, message=None):
        if not message:
            message = "Your password must contain at least one upper case letter, one lowercase letter, and one digit"
        self.message = message

    def __call__(self, form, field):
        schema = PasswordValidator()
        schema \
            .has().uppercase() \
            .has().lowercase() \
            .has().digits()
        if not schema.validate(field.data):
            raise ValidationError(self.message)


class RegistrationForm(FlaskForm) :
    username = StringField("Username",
                           [
                               DataRequired(message="Username required"),
                               Length(min = 3, message="Username must be at least 3 characters long")
                               #UsernameValid()
                           ])

    password = PasswordField("Password",
                           [
                               DataRequired(message="Password required"),
                               PasswordValid()
                           ])

    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    username = StringField('Username', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    submit = SubmitField('Login')