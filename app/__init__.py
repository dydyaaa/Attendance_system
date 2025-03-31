import os
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
migrate = Migrate()

def create_app():

    app = Flask(__name__)
    load_dotenv()
    app.config.from_prefixed_env()

    @app.route('/')
    def index():
        a = app.config['SECRET_KEY']
        return jsonify({'message': f'{a}'})

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'message': 'Not Found'}), 404
    
    @app.errorhandler(Exception)
    def internal_server_error(error):
        app.logger.error(f'{error}')
        return jsonify({'message': f'Internal Server Error'}), 500
    
    return app