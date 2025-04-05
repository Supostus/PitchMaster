from flask import Flask
import logging
from extensions import db, login_manager  # Импорт из нового файла
from routes.auth import auth_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pitchmaster.db'

# Инициализация расширений
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

# Настройка логирования
logging.basicConfig(filename='pitchmaster.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logging.info('Приложение PitchMaster запущено')

# Подключение маршрутов
app.register_blueprint(auth_bp, url_prefix='/auth')

# Импорт моделей после инициализации
from models import User, Objection

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Создаёт таблицы в базе данных
    app.run(debug=True)