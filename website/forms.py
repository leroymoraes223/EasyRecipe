from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash
from wtforms import StringField, TextAreaField, EmailField, PasswordField, SubmitField
from wtforms.validators import EqualTo, Length, DataRequired, Email, ValidationError
from .models import user

class UserRegistraionForm(FlaskForm):

    def validate_username(self, input):
        username = user.query.filter_by(USERNAME=input.data).first()
        if username:
            raise ValidationError("This Username is already in Use")

    def validate_email(self, input):
        email = user.query.filter_by(EMAIL=input.data).first()
        if email:
            raise ValidationError("This email is already in Use")

    username = StringField(label="Username", validators=[Length(min=6), DataRequired()])
    email = EmailField(label="Email", validators=[Email(), DataRequired()])
    password1 = PasswordField(label="Password", validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label="Confirm Password", validators=[EqualTo("password1")])
    submit = SubmitField(label="Create Account")

class UserLoginForm(FlaskForm):

    def validate(self, extra_validators=None):
        initial_validation = super(UserLoginForm, self).validate()
        if not initial_validation:
            return False
        User = user.query.filter_by(USERNAME=self.username.data).first()
        if User is None:
            self.username.errors.append("User with this Username Does not Exist")
            return False
        print(User)
        print(User.PASSWORD)
        print(self.password.data)
        if not check_password_hash(User.PASSWORD, self.password.data):               
            self.password.errors.append("Incorrecnt Password")
            return False
        self.user = User
        return True

    username = StringField(label="Username")
    password = PasswordField(label="Password")
    submit = SubmitField(label="Login")
