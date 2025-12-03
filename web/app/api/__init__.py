"""
API Blueprint for Dram Planner Web Application
"""

from flask import Blueprint

bp = Blueprint('api', __name__)

from app.api import bottles, schedules, config, auth, export, barcode, catalog, groups, whisky_sources, admin, health

