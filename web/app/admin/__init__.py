"""
Admin module for Dram Planner
"""

from flask import Blueprint

bp = Blueprint('admin', __name__, url_prefix='/admin')

from app.admin import routes

