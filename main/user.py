from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    jsonify,
    session,
    flash
)
from exts import mail, db
from flask_mail import Message
from models import EmailCaptchaModel, UserModel
import string
import random
from datetime import datetime
from .forms import LoginForm, RegisterForm
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint("user", __name__, url_prefix="/user")


# verify login information, get the data and check if validate
@bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = UserModel.query.filter_by(email=email).first()
            if user and check_password_hash(user.password, password):
                session['user_id'] = user.id
                return redirect("/")
            else:
                # username and password does not match
                flash("Password does not match the Email!")
                return redirect(url_for("user.login"))
        else:
            # format incorrect
            flash("Email or Password format is incorrect!")
            return redirect(url_for("user.login"))


# get the register data and stor into the database
# table user, email, username, password
@bp.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        form = RegisterForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data

            # password encryption processing
            hash_password = generate_password_hash(password)
            user = UserModel(email=email, username=username, password=hash_password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("user.login"))
        else:
            return redirect(url_for("user.register"))


# log out function, clear session, return to login page
@bp.route("/logout")
def logout():
    # clear all the data in session
    session.clear()
    return redirect(url_for('user.login'))


# post the verification code to the input email
@bp.route("/verification", methods=['POST'])
def get_verification():
    # GET, POST to get the email input
    email = request.form.get("email")
    veri_letters = string.ascii_letters + string.digits
    verification_code = "".join(random.sample(veri_letters, 4))
    if email:
        # verification code message
        message = Message(
            subject="Verification Code for the ToDoList",
            recipients=[email],
            body=f"[ToDoList] Your verification code for the registration is: {verification_code}, "
                 f"please do not tell anyone else."
        )
        mail.send(message)
        verification_model = EmailCaptchaModel.query.filter_by(email=email).first()
        # if exists, replace the code for specific email
        if verification_model:
            verification_model.verification_code = verification_code
            verification_model.create_time = datetime.now()
            db.session.commit()
        # if not, add a verification_model and commit to the database
        else:
            verification_model = EmailCaptchaModel(email=email, verification_code=verification_code)
            db.session.add(verification_model)
            db.session.commit()
        # print("verification_code:", verification_code)
        # return a successful request code: 200
        return jsonify({"code": 200})
    else:
        # return a client error code: 400
        return jsonify({"code": 400, "message": "Please pass the email first!"})
