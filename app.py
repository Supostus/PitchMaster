from flask import Flask
import logging
from extensions import db, login_manager
from routes.auth import auth_bp
from routes.test import test_bp
from models import User
import os  # Добавь этот импорт

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'pitchmaster.db')  # Явный путь

db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

logging.basicConfig(filename='pitchmaster.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logging.info('Приложение PitchMaster запущено')

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(test_bp, url_prefix='/test')

from models import User, Objection

def create_test_user():
    with app.app_context():
        db.drop_all()
        db.create_all()
        if not User.query.filter_by(email='test@example.com').first():
            test_user = User(email='test@example.com', password='test123')
            db.session.add(test_user)
            db.session.commit()
            logging.info('Тестовый пользователь создан')

if __name__ == '__main__':
    create_test_user()
    with app.app_context():
        db.create_all()
    app.run(debug=True)