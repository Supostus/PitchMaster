from flask import Blueprint, render_template, request, redirect, url_for
from extensions import db
from models import User
from flask_login import login_required, current_user

test_bp = Blueprint('test', __name__, template_folder='../templates')

@test_bp.route('/test', methods=['GET', 'POST'])
@login_required
def test():
    if request.method == 'POST':
        name = request.form['name']
        position = request.form['position']
        product = request.form['product']
        utp = request.form['utp']
        lpr_position = request.form['lpr_position']
        objections = request.form.getlist('objections')

        current_user.name = name
        current_user.position = position
        current_user.product = product
        current_user.utp = utp
        current_user.lpr_position = lpr_position
        db.session.commit()

        return redirect(url_for('dashboard.dashboard'))  # Изменён редирект
    return render_template('test.html')