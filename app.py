from flask import Flask
from flask_login import LoginManager
from extensions import db, bcrypt
from routes.auth import auth_bp
from routes.test import test_bp
from routes.dashboard import dashboard_bp
import logging

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pitchmaster.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Инициализация расширений
db.init_app(app)
bcrypt.init_app(app)

# Настройка логирования
logging.basicConfig(filename='pitchmaster.log', level=logging.INFO)

# Настройка Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

from models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Регистрация blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(test_bp, url_prefix='/test')
app.register_blueprint(dashboard_bp, url_prefix='/dashboard')

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)