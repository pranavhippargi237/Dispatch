from flask import Blueprint

# Create blueprints
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
daily_sheet_bp = Blueprint('daily_sheet', __name__, url_prefix='/daily-sheet')
employee_bp = Blueprint('employee', __name__, url_prefix='/employee')
equipment_bp = Blueprint('equipment', __name__, url_prefix='/equipment')

# Import routes
from . import auth_routes, daily_sheet_routes, employee_routes, equipment_routes