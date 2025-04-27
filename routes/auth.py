from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from models import User
from extensions import db, bcrypt
import logging

auth_bp = Blueprint('auth', __name__, template_folder='../templates')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            logging.info(f"Пользователь {email} успешно вошёл")
            return redirect(url_for('dashboard.dashboard'))
        else:
            flash('Неверный email или пароль', 'danger')
            logging.warning(f"Неудачная попытка входа для {email}")
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if User.query.filter_by(email=email).first():
            flash('Email уже зарегистрирован', 'danger')
            logging.warning(f"Попытка регистрации с существующим email: {email}")
        else:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            user = User(email=email, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash('Регистрация успешна! Войдите в систему.', 'success')
            logging.info(f"Новый пользователь зарегистрирован: {email}")
            return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    logging.info("Пользователь вышел из системы")
    flash('Вы вышли из системы', 'success')
    return redirect(url_for('auth.login'))