"""
Security configuration and middleware for Dram Planner
Part of ENH-013: Security & Vulnerability Assessment
"""

from flask_talisman import Talisman
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from functools import wraps
from flask import request, jsonify, current_app

# Security headers configuration
security_headers = {
    'strict_transport_security': {
        'max_age': 31536000,
        'include_subdomains': True,
        'preload': True
    },
    'content_security_policy': {
        'default-src': "'self'",
        'script-src': "'self' 'unsafe-inline'",
        'style-src': "'self' 'unsafe-inline'",
        'img-src': "'self' data: https:",
        'font-src': "'self'",
        'connect-src': "'self'"
    },
    'x_content_type_options': 'nosniff',
    'x_frame_options': 'SAMEORIGIN',
    'x_xss_protection': '1; mode=block',
    'referrer_policy': 'strict-origin-when-cross-origin'
}

def init_security(app):
    """Initialize security extensions."""
    # Initialize Talisman for security headers
    Talisman(
        app,
        force_https=app.config.get('FORCE_HTTPS', False),
        strict_transport_security=True,
        strict_transport_security_max_age=31536000,
        content_security_policy=security_headers['content_security_policy'],
        content_security_policy_nonce_in=['script-src'],
        frame_options='SAMEORIGIN',
        x_content_type_options=True,
        referrer_policy='strict-origin-when-cross-origin'
    )
    
    # Initialize rate limiter
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"],
        storage_uri="memory://",
        headers_enabled=True
    )
    
    # Custom rate limits for specific endpoints
    limiter.limit("10 per minute")(app.view_functions.get('auth.register'))
    limiter.limit("20 per minute")(app.view_functions.get('auth.login'))
    
    return limiter


def rate_limit_exceeded_handler(e):
    """Handle rate limit exceeded errors."""
    return jsonify({
        'error': 'Rate limit exceeded',
        'message': 'Too many requests. Please try again later.'
    }), 429


def validate_input(data, required_fields=None, field_types=None):
    """Validate input data to prevent injection attacks."""
    if required_fields:
        for field in required_fields:
            if field not in data:
                return False, f"Missing required field: {field}"
    
    if field_types:
        for field, expected_type in field_types.items():
            if field in data and not isinstance(data[field], expected_type):
                return False, f"Invalid type for field: {field}"
    
    return True, None


def sanitize_string(value):
    """Sanitize string input to prevent XSS."""
    if not isinstance(value, str):
        return value
    
    # Remove potentially dangerous characters
    dangerous = ['<', '>', '"', "'", '&', '\x00']
    for char in dangerous:
        if char in value:
            # HTML escape
            value = value.replace('<', '&lt;')
            value = value.replace('>', '&gt;')
            value = value.replace('"', '&quot;')
            value = value.replace("'", '&#x27;')
            value = value.replace('&', '&amp;')
    
    return value.strip()


def require_https(f):
    """Decorator to require HTTPS in production."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_app.config.get('FORCE_HTTPS') and not request.is_secure:
            return jsonify({'error': 'HTTPS required'}), 403
        return f(*args, **kwargs)
    return decorated_function

