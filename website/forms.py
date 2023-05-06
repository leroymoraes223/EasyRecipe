from flask_wtf import FlaskForm
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

