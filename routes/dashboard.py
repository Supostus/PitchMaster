from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models import User, Objection

dashboard_bp = Blueprint('dashboard', __name__, template_folder='../templates')

@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    user = current_user
    return render_template('dashboard.html', user=user)

@dashboard_bp.route('/call')
@login_required
def call():
    user = current_user
    script = f"Здравствуйте, Имя! Меня зовут {user.name}, я {user.position} из SalesPro. Мы предлагаем {user.product} — {user.utp}. Есть пара минут?"
    return render_template('call.html', script=script)