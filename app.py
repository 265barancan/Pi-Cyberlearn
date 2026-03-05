from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, login_required, current_user
from config import Config
from models.database import init_db
from models.user import User
from blueprints.auth import auth_bp
from blueprints.lessons import lessons_bp
from blueprints.quiz import quiz_bp
from blueprints.ai_tutor import ai_bp
from blueprints.terminal import terminal_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Init database
    init_db(app)

    # Setup Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = "Lütfen önce giriş yapın."
    login_manager.login_message_category = "error"

    @login_manager.user_loader
    def load_user(user_id):
        return User.get(user_id)

    # Register Blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(lessons_bp, url_prefix='/lessons')
    app.register_blueprint(quiz_bp, url_prefix='/quiz')
    app.register_blueprint(ai_bp, url_prefix='/ai')
    app.register_blueprint(terminal_bp, url_prefix='/terminal')

    @app.route('/')
    @login_required
    def index():
        return render_template('index.html', user=current_user)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
