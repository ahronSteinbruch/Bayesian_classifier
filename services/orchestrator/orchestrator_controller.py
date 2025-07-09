from flask import Blueprint

bp = Blueprint(__name__)

@bp.route('/')
def index():
    return {'status': 'OK'}
