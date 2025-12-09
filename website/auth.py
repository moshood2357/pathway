from functools import wraps

from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from flask_mail import Message
import random
from website.models import User,db, User
from website import mail
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError

from website.forms import RegistrationForm, LoginForm,ResetForm,OtpForm,ResetPasswordForm



auth = Blueprint('auth', __name__)
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please log in to continue.", "errormsg")
            return redirect(url_for('auth.Sign_in'))
        return f(*args, **kwargs)
    return decorated_function

@auth.after_request
def after_request(response):
    """
    Runs after each request.
    Disables caching to prevent viewing protected
    pages after logout using the back button.
    """
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response


@auth.route("/sign-in", methods=['GET', 'POST'])
def Sign_in():

    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        record = User.query.filter(User.email==email).first()

        if record:
            if check_password_hash(record.password_hash, password):
                session['user_id'] = record.user_id

                # flash('Login successful!', category='msg')
                return redirect(url_for('views.dashboard'))

            else:
                flash('Incorrect password. Please try again.', category='errormsg')
                return redirect(url_for('auth.Sign_in'))
        else:
            flash('No account found with that email.', category='errormsg')
            return redirect(url_for('auth.Sign_in'))

    return render_template("signin.html", form=form)

@auth.route("/sign-up", methods=['GET', 'POST'])
def Sign_up():
    # Redirect logged-in users away from signup
    if session.get('user_id'):
        return redirect(url_for('views.dashboard'))

    form = RegistrationForm()

    if form.validate_on_submit():  
        fullname = form.name.data
        user_email = form.email.data
        password = form.password.data

        hashed_password = generate_password_hash(password)

        u = User(full_name=fullname, email=user_email, password_hash=hashed_password)

        try:
            db.session.add(u)
            db.session.commit()
            
            session['user_id'] = u.user_id
            return redirect(url_for('views.Second_question'))
        except:
            db.session.rollback()
            flash('Email is taken.', category='errormsg')
            return redirect(url_for('auth.Sign_up'))

    return render_template('signup.html', form=form)
    



@auth.route("/reset-email", methods=['GET', 'POST'])
def Reset_email():
    form = ResetForm()

    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter(User.email == email).first()

        if user:
    
            otp = random.randint(100000, 999999)

            # Store email and OTP in session temporarily
            session['reset_email'] = email
            session['otp'] = otp

            # Send OTP to email
            msg = Message("Password Reset OTP", recipients=[email])
            msg.body = f"Your OTP code is {otp}. It will expire in 10 minutes."
            mail.send(msg)

            flash("An OTP has been sent to your email.", "msg")
            return redirect(url_for('auth.Reset_otp'))
        else:
            flash("No account found with that email address.", "errormsg")

    return render_template("reset.html", form=form)

@auth.route("/resetotp", methods=['GET', 'POST'])
def Reset_otp():
    form = OtpForm()
    if form.validate_on_submit():
        return redirect(url_for('auth.Reset_password'))
    if request.method == "POST":
        pass
        # flash("OTP does not match. Please check your input.", "errormsg")

    return render_template("resetotp.html", form=form)


@auth.route("/resetpassword", methods=['GET', 'POST'])
def Reset_password():
    form = ResetPasswordForm()

    return render_template("resetpassword.html", form=form)



@auth.route('/logout/')
def logout():
    session.pop('user_id', None) 
    # flash("You have been logged out.", "success")
    return redirect(url_for('views.home'))
