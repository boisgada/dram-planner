"""
Health check and monitoring endpoints
Part of ENH-014: Production Deployment & Infrastructure
"""

from flask import jsonify
from app.api import bp
from app import db
from datetime import datetime


@bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for monitoring and load balancers."""
    try:
        # Check database connectivity
        db.session.execute('SELECT 1')
        db_status = 'healthy'
    except Exception as e:
        db_status = f'unhealthy: {str(e)}'
    
    return jsonify({
        'status': 'healthy' if db_status == 'healthy' else 'degraded',
        'timestamp': datetime.utcnow().isoformat(),
        'checks': {
            'database': db_status,
            'application': 'healthy'
        }
    }), 200 if db_status == 'healthy' else 503


@bp.route('/health/ready', methods=['GET'])
def readiness_check():
    """Readiness check - indicates if application is ready to serve traffic."""
    try:
        db.session.execute('SELECT 1')
        return jsonify({
            'status': 'ready',
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    except Exception:
        return jsonify({
            'status': 'not ready',
            'timestamp': datetime.utcnow().isoformat()
        }), 503


@bp.route('/health/live', methods=['GET'])
def liveness_check():
    """Liveness check - indicates if application is alive."""
    return jsonify({
        'status': 'alive',
        'timestamp': datetime.utcnow().isoformat()
    }), 200

