# Docker Deployment Guide

Dram Planner Web Application can be deployed as a self-contained Docker container.

## Quick Start

**This is the only supported way to run the web application.**

### Development (with hot-reload)

```bash
# Build and run development container
cd web
docker-compose -f docker-compose.dev.yml up --build

# Access at http://localhost:5000
```

**First time setup:**
```bash
# Initialize database (in another terminal while container is running)
docker-compose -f docker-compose.dev.yml exec web flask db init
docker-compose -f docker-compose.dev.yml exec web flask db migrate -m "Initial migration"
docker-compose -f docker-compose.dev.yml exec web flask db upgrade
```

### Production

```bash
# Set environment variables
export SECRET_KEY=your-secret-key-here
export DB_PASSWORD=your-db-password

# Build and run
docker-compose up -d --build

# Initialize database
docker-compose exec web flask db upgrade

# View logs
docker-compose logs -f web
```

## Docker Compose Services

### Production (`docker-compose.yml`)

- **web**: Flask application (Gunicorn)
- **db**: PostgreSQL database

### Development (`docker-compose.dev.yml`)

- **web**: Flask development server with hot-reload
- Uses SQLite for simplicity

## Environment Variables

Create a `.env` file or set environment variables:

```bash
# Required
SECRET_KEY=your-secret-key-here
DB_PASSWORD=your-database-password

# Optional
FLASK_ENV=production
DATABASE_URL=postgresql://user:pass@db:5432/dbname
```

## Database Migrations

### First Time Setup

```bash
# Initialize migrations
docker-compose exec web flask db init

# Create initial migration
docker-compose exec web flask db migrate -m "Initial migration"

# Apply migration
docker-compose exec web flask db upgrade
```

### Subsequent Migrations

```bash
# Create migration
docker-compose exec web flask db migrate -m "Description"

# Apply migration
docker-compose exec web flask db upgrade
```

## Building Images

### Production Image

```bash
docker build -t dram-planner:latest .
```

### Development Image

```bash
docker build -f Dockerfile.dev -t dram-planner:dev .
```

## Running Containers

### Production

```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

### Development

```bash
# Start with hot-reload
docker-compose -f docker-compose.dev.yml up

# Run in background
docker-compose -f docker-compose.dev.yml up -d
```

## Accessing the Application

- **Web UI**: http://localhost:5000
- **API**: http://localhost:5000/api
- **Database**: localhost:5432 (PostgreSQL)

## Container Management

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f web
```

### Execute Commands

```bash
# Shell access
docker-compose exec web bash

# Run Flask commands
docker-compose exec web flask db upgrade
docker-compose exec web flask shell
```

### Database Access

```bash
# PostgreSQL shell
docker-compose exec db psql -U dramplanner -d dramplanner
```

## Volumes

The following directories are mounted as volumes:

- `./uploads` - User uploaded files (photos)
- `./exports` - Exported data files
- `./instance` - Application instance data (SQLite in dev)
- `postgres_data` - PostgreSQL data (production)

## Production Deployment

### Recommended Setup

1. **Use PostgreSQL** (included in docker-compose.yml)
2. **Set strong SECRET_KEY** via environment variable
3. **Use reverse proxy** (nginx) for SSL/TLS
4. **Set up backups** for database volume
5. **Configure logging** to external service

### Example nginx Configuration

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Troubleshooting

### Container won't start

```bash
# Check logs
docker-compose logs web

# Check if port is in use
lsof -i :5000
```

### Database connection issues

```bash
# Check database is running
docker-compose ps db

# Check database logs
docker-compose logs db

# Test connection
docker-compose exec web python -c "from app import db; print(db.engine.url)"
```

### Permission issues

```bash
# Fix uploads directory permissions
sudo chown -R $USER:$USER uploads exports instance
```

## Security Considerations

1. **Never commit `.env` files** - Use environment variables or secrets management
2. **Use strong SECRET_KEY** - Generate with: `python -c "import secrets; print(secrets.token_hex(32))"`
3. **Keep images updated** - Regularly rebuild with latest base images
4. **Use HTTPS** - Configure reverse proxy with SSL certificates
5. **Limit exposed ports** - Only expose necessary ports
6. **Database security** - Use strong passwords, limit network access

## Scaling

For production scaling, consider:

- **Multiple web containers** behind a load balancer
- **Separate database server** (not in same compose file)
- **Redis** for session storage and caching
- **CDN** for static assets

## Backup and Restore

### Backup Database

```bash
# PostgreSQL backup
docker-compose exec db pg_dump -U dramplanner dramplanner > backup.sql

# Or using volume backup
docker run --rm -v dram-planner_postgres_data:/data -v $(pwd):/backup \
  alpine tar czf /backup/postgres_backup.tar.gz /data
```

### Restore Database

```bash
# PostgreSQL restore
docker-compose exec -T db psql -U dramplanner dramplanner < backup.sql
```

---

For more information, see the main [README.md](README.md)

