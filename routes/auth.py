from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user
from models import User

auth_bp = Blueprint('auth', __name__, template_folder='../templates')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:  # Простая проверка
            login_user(user)
            return redirect(url_for('test.test'))
    return render_template('login.html')