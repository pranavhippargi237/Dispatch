from flask import Flask
from flask_login import LoginManager
from firebase_admin import credentials, initialize_app
from .config import Config

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize Firebase
    cred = credentials.Certificate(app.config['FIREBASE_CREDENTIALS'])
    initialize_app(cred)
    
    # Initialize Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    # Register blueprints
    from .routes import auth_bp, daily_sheet_bp, employee_bp, equipment_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(daily_sheet_bp)
    app.register_blueprint(employee_bp)
    app.register_blueprint(equipment_bp)
    
    return app