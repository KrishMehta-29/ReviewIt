from flask import Blueprint

github_bp = Blueprint('github', __name__, url_prefix='/')

from . import routes  # Import routes after defining the blueprint