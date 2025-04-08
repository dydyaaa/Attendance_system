import os
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect


db = SQLAlchemy()
migrate = Migrate()

def create_app():

    app = Flask(__name__)
    load_dotenv()
    app.config.from_prefixed_env()

    db.init_app(app)
    migrate.init_app(app, db)
    csrf = CSRFProtect(app)

    from app.routes.attendance import attendance_bp
    app.register_blueprint(attendance_bp)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'message': 'Not Found'}), 404
    
    @app.errorhandler(Exception)
    def internal_server_error(error):
        app.logger.error(f'{error}')
        return jsonify({'message': f'Internal Server Error'}), 500
    
    return app