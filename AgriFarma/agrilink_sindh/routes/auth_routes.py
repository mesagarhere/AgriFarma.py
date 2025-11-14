from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from agrilink_sindh.models.user_model import User
from agrilink_sindh.extensions import db

auth = Blueprint('auth', __name__)


# -------------------------
# LOGIN
# -------------------------
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if not user:
            flash("User does not exist!", "danger")
            return redirect(url_for('auth.login'))

        if not user.check_password(password):
            flash("Incorrect password!", "danger")
            return redirect(url_for('auth.login'))

        login_user(user)
        return redirect(url_for('dashboard.dashboard_home'))   # ✅ STEP 3 FIXED

    return render_template('login.html')


# -------------------------
# REGISTER
# -------------------------
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')

        # Check if email exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered!", "warning")
            return redirect(url_for('auth.register'))

        # Create new user and set password via model helper
        new_user = User(name=name, email=email, role=role)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        flash("Account created successfully! Please log in.", "success")
        return redirect(url_for('auth.login'))

    return render_template('register.html')


# -------------------------
# LOGOUT
# -------------------------
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
