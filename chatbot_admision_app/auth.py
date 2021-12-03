from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import check_password_hash
from flask_login import login_user, login_required,logout_user
import hashlib

from . import db
from .models import User

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    # login code goes here
    username = request.form.get('username')
    print(username)
    password = request.form.get('password')
    print(password)
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(username=username).first()
    print(user)
    password = password.encode('utf-8')
    check_password = (user.password == hashlib.sha256(password).hexdigest())
    print(hashlib.sha256(password).hexdigest())
    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password:
        flash('Credenciales incorrectas, intenta de nuevo')
        return redirect(url_for('auth.login'))  # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    # Enviar al dashboard una vez se haya autenticado
    return redirect("/dashapp")

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    print("cerrando sesión")
    return redirect(url_for("index_get"))