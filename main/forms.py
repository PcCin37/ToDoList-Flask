# create the basic form to store the data and the important validators for the data

import wtforms
from wtforms.validators import length, email, EqualTo
from models import EmailCaptchaModel, UserModel


# login form use for storing login information
# validators for each element
# email, password
class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[email(message="Wrong format for login email!")])
    password = wtforms.StringField(validators=[length(min=8, max=20, message="Wrong format for password!")])


# register form use for storing register information
# validators for each element
# username, email, verification code, password
class RegisterForm(wtforms.Form):
    username = wtforms.StringField(validators=[length(min=4, max=20, message="Wrong format for username!")])
    email = wtforms.StringField(validators=[email(message="Wrong format for email!")])
    verification_code = wtforms.StringField(validators=[length(min=4, max=4,
                                                               message="Wrong format for verification code!")])
    password = wtforms.StringField(validators=[length(min=8, max=20, message="Wrong format for password!")])
    confirm_password = wtforms.StringField(validators=[EqualTo("password")])

    # check if the verification code is correct, if not raise error information
    def validate_verification_code(self, field):
        verification_code = field.data
        email = self.email.data
        verification_model = EmailCaptchaModel.query.filter_by(email=email).first()
        if not verification_model or verification_model.verification_code.lower() != verification_code.lower():
            raise wtforms.ValidationError("Wrong Verification Code!")

    # check if the email address is registered, if yes raise error
    def validate_email(self, field):
        email = field.data
        user_model = UserModel.query.filter_by(email=email).first()
        if user_model:
            raise wtforms.ValidationError("The email address has already been registered!")


# todolist form use for storing list information
# validators for each element
# assessment title, module title, deadline, importance, status, description
class TodolistForm(wtforms.Form):
    assessment_title = wtforms.StringField(validators=[length(min=2, max=200,
                                                              message="Wrong format for assessment title!")])
    module = wtforms.StringField(validators=[length(min=1, message="Wrong format for module code!")])
    deadline = wtforms.DateTimeField(validators=[])
    importance = wtforms.StringField()
    status = wtforms.StringField()
    description = wtforms.StringField(validators=[length(min=1, message="Wrong format for description!")])
