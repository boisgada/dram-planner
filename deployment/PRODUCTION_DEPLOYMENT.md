# Production Deployment Guide

**Part of ENH-014: Production Deployment & Infrastructure**

This guide documents the production deployment process for Dram Planner at www.dram-planner.com.

---

## Prerequisites

- Domain registered: www.dram-planner.com ✅
- Server: vps05 (current) or dedicated server
- Docker containers configured ✅
- SSL certificate setup needed
- Nginx reverse proxy configuration needed

---

## Deployment Checklist

### 1. Infrastructure Setup
- [ ] Server capacity assessment
- [ ] DNS configuration (CNAME/A record)
- [ ] SSL certificate provisioning (Let's Encrypt)
- [ ] Firewall configuration
- [ ] Backup strategy

### 2. Application Configuration
- [ ] Environment variables setup
- [ ] Production database configuration
- [ ] Secret key management
- [ ] Static file serving configuration
- [ ] Media file storage

### 3. Security Hardening
- [ ] SSL/TLS configuration
- [ ] Security headers (already implemented ✅)
- [ ] Rate limiting (already implemented ✅)
- [ ] Database connection security
- [ ] File upload restrictions

### 4. Monitoring & Maintenance
- [ ] Application monitoring setup
- [ ] Error tracking
- [ ] Log aggregation
- [ ] Automated backups
- [ ] Health check endpoints

### 5. Go-Live
- [ ] Staging environment testing
- [ ] Load testing
- [ ] Rollback procedures
- [ ] User communication

---

## Deployment Steps

### Step 1: SSL Certificate Setup

```bash
# Install certbot
sudo apt-get update
sudo apt-get install certbot python3-certbot-nginx

# Obtain SSL certificate
sudo certbot --nginx -d www.dram-planner.com -d dram-planner.com
```

### Step 2: Nginx Configuration

Create `/etc/nginx/sites-available/dram-planner`:

```nginx
server {
    listen 80;
    server_name www.dram-planner.com dram-planner.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name www.dram-planner.com dram-planner.com;

    ssl_certificate /etc/letsencrypt/live/www.dram-planner.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/www.dram-planner.com/privkey.pem;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Proxy to Flask application
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Static files
    location /static {
        alias /path/to/dram-planner/web/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # File uploads
    client_max_body_size 16M;
}
```

### Step 3: Environment Variables

Create `.env.production`:

```bash
FLASK_ENV=production
SECRET_KEY=<generate-strong-secret-key>
DATABASE_URL=postgresql://user:pass@localhost/dramplanner
FORCE_HTTPS=true
```

---

## Monitoring

### Health Check Endpoint

Add to `web/app/api/__init__.py` or create `web/app/api/health.py`:

```python
@bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for monitoring."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat()
    }), 200
```

---

## Backup Strategy

### Automated Database Backups

Create backup script and schedule with cron:

```bash
#!/bin/bash
# backup_db.sh
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/dram-planner"
mkdir -p $BACKUP_DIR

# PostgreSQL backup
pg_dump $DATABASE_URL > "$BACKUP_DIR/db_backup_$DATE.sql"

# Keep only last 7 days
find $BACKUP_DIR -name "db_backup_*.sql" -mtime +7 -delete
```

---

## Rollback Procedure

1. Stop current containers
2. Switch DNS/load balancer to previous version
3. Restore database from backup if needed
4. Restart previous version containers

---

**Status:** Documentation complete, ready for implementation

