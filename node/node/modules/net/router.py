from flask import Blueprint
router = Blueprint('net', __name__)

@router.route('/')
def index():
    return 'Hello world!'