from flask import Blueprint, render_template

terminal_bp = Blueprint('terminal', __name__)

@terminal_bp.route('/')
def index():
    return render_template('terminal.html')
