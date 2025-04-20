from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from models import User, Objection
from extensions import db
import logging

dashboard_bp = Blueprint('dashboard', __name__, template_folder='../templates')

@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    user = current_user
    return render_template('dashboard.html', user=user)

@dashboard_bp.route('/call', methods=['GET', 'POST'])
@login_required
def call():
    user = current_user
    stage = request.form.get('stage', 'greeting')  # Текущая стадия звонка
    response = request.form.get('response')  # Реакция ЛПР

    # Начальные данные для карточки
    script = ""
    buttons = []
    next_stage = stage

    # Проверяем пользовательские возражения
    objections = Objection.query.filter_by(user_id=user.id).all()
    custom_objection_stages = [f"objection_{obj.objection.replace(' ', '_')}" for obj in objections]

    if stage == 'greeting':
        script = f"Здравствуйте, Имя! Меня зовут {user.name}, я {user.position} из SalesPro. Мы предлагаем {user.product} — {user.utp}. Есть пара минут?"
        buttons = [
            {'value': 'yes', 'text': 'Да, интересно', 'class': 'btn-success'},
            {'value': 'no_time', 'text': 'Нет времени', 'class': 'btn-warning'},
            {'value': 'has_solution', 'text': 'Уже есть решение', 'class': 'btn-warning'},
            {'value': 'not_interested', 'text': 'Не интересно', 'class': 'btn-danger'}
        ] + [{'value': f"objection_{obj.objection.replace(' ', '_')}", 'text': obj.objection, 'class': 'btn-warning'} for obj in objections]
        if response == 'yes':
            next_stage = 'presentation'
        elif response == 'no_time':
            next_stage = 'no_time'
        elif response == 'has_solution':
            next_stage = 'has_solution'
        elif response == 'not_interested':
            next_stage = 'not_interested'
        elif response in custom_objection_stages:
            next_stage = response

    elif stage == 'presentation':
        script = f"Отлично, Имя! Наш {user.product} помогает {user.utp}. Хотите узнать подробности?"
        buttons = [
            {'value': 'agree_meeting', 'text': 'Согласен на встречу', 'class': 'btn-success'},
            {'value': 'expensive', 'text': 'Дорого', 'class': 'btn-warning'},
            {'value': 'think', 'text': 'Подумаю', 'class': 'btn-warning'},
        ] + [{'value': f"objection_{obj.objection.replace(' ', '_')}", 'text': obj.objection, 'class': 'btn-warning'} for obj in objections]
        if response == 'agree_meeting':
            next_stage = 'closing'
        elif response == 'expensive':
            next_stage = 'expensive'
        elif response == 'think':
            next_stage = 'think'
        elif response in custom_objection_stages:
            next_stage = response

    elif stage == 'no_time':
        script = f"Понимаю, Имя, что у вас мало времени. Когда удобно перезвонить?"
        buttons = [
            {'value': 'morning', 'text': '10:00', 'class': 'btn-success'},
            {'value': 'evening', 'text': '17:00', 'class': 'btn-success'},
            {'value': 'no_call', 'text': 'Не перезванивайте', 'class': 'btn-danger'}
        ] + [{'value': f"objection_{obj.objection.replace(' ', '_')}", 'text': obj.objection, 'class': 'btn-warning'} for obj in objections]
        if response in ['morning', 'evening']:
            next_stage = 'closing'
        elif response == 'no_call':
            next_stage = 'not_interested'
        elif response in custom_objection_stages:
            next_stage = response

    elif stage == 'has_solution':
        script = f"Понимаю, Имя, что у вас есть решение. Наш {user.product} интегрируется и усиливает {user.utp}."
        buttons = [
            {'value': 'interested', 'text': 'Интересно', 'class': 'btn-success'},
            {'value': 'expensive', 'text': 'Дорого', 'class': 'btn-warning'},
            {'value': 'think', 'text': 'Подумаю', 'class': 'btn-warning'}
        ] + [{'value': f"objection_{obj.objection.replace(' ', '_')}", 'text': obj.objection, 'class': 'btn-warning'} for obj in objections]
        if response == 'interested':
            next_stage = 'presentation'
        elif response == 'expensive':
            next_stage = 'expensive'
        elif response == 'think':
            next_stage = 'think'
        elif response in custom_objection_stages:
            next_stage = response

    elif stage == 'expensive':
        script = f"Понимаю, Имя, что цена важна. Наш {user.product} окупается благодаря {user.utp}."
        buttons = [
            {'value': 'interested', 'text': 'Интересно', 'class': 'btn-success'},
            {'value': 'think', 'text': 'Подумаю', 'class': 'btn-warning'}
        ] + [{'value': f"objection_{obj.objection.replace(' ', '_')}", 'text': obj.objection, 'class': 'btn-warning'} for obj in objections]
        if response == 'interested':
            next_stage = 'presentation'
        elif response == 'think':
            next_stage = 'think'
        elif response in custom_objection_stages:
            next_stage = response

    elif stage == 'think':
        script = f"Хорошо, Имя, понимаю, что нужно время. Могу отправить презентацию о {user.product} на почту?"
        buttons = [
            {'value': 'send', 'text': 'Отправить', 'class': 'btn-success'},
            {'value': 'no', 'text': 'Нет, спасибо', 'class': 'btn-danger'}
        ] + [{'value': f"objection_{obj.objection.replace(' ', '_')}", 'text': obj.objection, 'class': 'btn-warning'} for obj in objections]
        if response == 'send':
            next_stage = 'closing'
        elif response == 'no':
            next_stage = 'not_interested'
        elif response in custom_objection_stages:
            next_stage = response

    elif stage == 'not_interested':
        script = f"Спасибо за внимание, Имя! Если передумаете, свяжитесь с нами по поводу {user.product}."
        buttons = [
            {'value': 'end', 'text': 'Завершить звонок', 'class': 'btn-secondary'}
        ]
        if response == 'end':
            return redirect(url_for('dashboard.dashboard'))

    elif stage == 'closing':
        script = f"Отлично, Имя! Давайте договоримся о встрече по {user.product} на завтра в 14:00?"
        buttons = [
            {'value': 'end', 'text': 'Завершить звонок', 'class': 'btn-secondary'}
        ]
        if response == 'end':
            return redirect(url_for('dashboard.dashboard'))

    # Обработка пользовательских возражений
    elif stage in custom_objection_stages:
        objection_text = stage.replace('objection_', '').replace('_', ' ')
        objection = Objection.query.filter_by(user_id=user.id, objection=objection_text).first()
        if objection:
            script = objection.response
            buttons = [
                {'value': 'interested', 'text': 'Интересно', 'class': 'btn-success'},
                {'value': 'think', 'text': 'Подумаю', 'class': 'btn-warning'},
                {'value': 'not_interested', 'text': 'Не интересно', 'class': 'btn-danger'}
            ]
            if response == 'interested':
                next_stage = 'presentation'
            elif response == 'think':
                next_stage = 'think'
            elif response == 'not_interested':
                next_stage = 'not_interested'

    return render_template('call.html', script=script, buttons=buttons, stage=next_stage)

@dashboard_bp.route('/add_objection', methods=['POST'])
@login_required
def add_objection():
    new_objection = request.form.get('new_objection')
    stage = request.form.get('stage')
    user = current_user

    logging.info(f"Получен запрос на добавление возражения: new_objection='{new_objection}', stage='{stage}', user='{user.email}'")
    
    if new_objection:
        try:
            objection = Objection(
                user_id=user.id,
                objection=new_objection,
                response=f"Понимаю, Имя, что {new_objection}. Вот как мы это решаем: наш {user.product} предлагает {user.utp}."
            )
            db.session.add(objection)
            db.session.commit()
            logging.info(f"Возражение '{new_objection}' успешно сохранено для пользователя {user.email}")
        except Exception as e:
            logging.error(f"Ошибка при сохранении возражения: {str(e)}")
            db.session.rollback()
    else:
        logging.warning("Новое возражение не было отправлено в форме (пустое поле)")

    return redirect(url_for('dashboard.call', stage=stage))