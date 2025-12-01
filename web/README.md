# Dram Planner Web Application

Web interface for Dram Planner built with Flask.

## Features

- RESTful API for all operations
- User authentication and accounts
- Collection management via web UI
- Schedule viewing and management
- Responsive design (mobile-friendly)
- Database-backed (SQLite/PostgreSQL)

## Setup

### 1. Install Dependencies

```bash
cd web
pip install -r requirements.txt
```

### 2. Set Environment Variables

Create a `.env` file:

```bash
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///dram_planner.db
```

### 3. Initialize Database

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 4. Run Application

```bash
python run.py
```

Or using Flask CLI:

```bash
export FLASK_APP=run.py
flask run
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login
- `POST /api/auth/logout` - Logout
- `GET /api/auth/me` - Get current user

### Bottles
- `GET /api/bottles` - List bottles (with pagination, filtering)
- `GET /api/bottles/<id>` - Get bottle
- `POST /api/bottles` - Create bottle
- `PUT /api/bottles/<id>` - Update bottle
- `DELETE /api/bottles/<id>` - Delete bottle
- `POST /api/bottles/<id>/tasting` - Record tasting
- `GET /api/bottles/stats` - Get collection statistics

### Schedules
- `GET /api/schedules` - List schedules
- `GET /api/schedules/<id>` - Get schedule
- `POST /api/schedules` - Generate schedule
- `DELETE /api/schedules/<id>` - Delete schedule
- `POST /api/schedules/<id>/items/<item_id>/complete` - Complete item

### Configuration
- `GET /api/config` - Get user config
- `PUT /api/config` - Update user config

## Development

### Database Migrations

```bash
# Create migration
flask db migrate -m "Description"

# Apply migration
flask db upgrade

# Rollback migration
flask db downgrade
```

### Testing

```bash
# Run tests (when implemented)
pytest
```

## Deployment

### Docker (Recommended)

The application is containerized for easy deployment. See [DOCKER.md](DOCKER.md) for detailed instructions.

**Quick Start:**
```bash
# Production
docker-compose up -d

# Development
docker-compose -f docker-compose.dev.yml up
```

### Traditional Deployment

1. Set `FLASK_ENV=production`
2. Use PostgreSQL: `DATABASE_URL=postgresql://...`
3. Set strong `SECRET_KEY`
4. Use production WSGI server (gunicorn)

```bash
gunicorn -w 4 -b 0.0.0.0:8000 run:app
```

## Project Structure

```
web/
├── app/
│   ├── __init__.py       # Application factory
│   ├── models.py         # Database models
│   ├── api/              # API endpoints
│   ├── auth/             # Authentication
│   ├── main/             # Main routes
│   ├── templates/        # HTML templates
│   └── static/           # CSS, JS, images
├── config.py             # Configuration
├── run.py                # Application entry point
└── requirements.txt      # Dependencies
```

## Notes

- The web application maintains backward compatibility with the CLI tool
- Data can be exported/imported between CLI and web versions
- User data is isolated per account
- All API endpoints require authentication (except registration/login)

