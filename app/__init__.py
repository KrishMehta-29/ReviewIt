from flask import Flask
from config import config
from app.blueprints.github import github_bp


def createApp(configName='default'):
    """Application factory function"""
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(config[configName])

    app.register_blueprint(github_bp)

    return app