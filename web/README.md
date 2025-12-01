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

**This application uses Docker exclusively.** See [DOCKER.md](DOCKER.md) for detailed instructions.

### Quick Start

```bash
# Development (with hot-reload)
docker-compose -f docker-compose.dev.yml up --build

# Production
docker-compose up --build
```

The application will be available at http://localhost:5000

### First Time Setup

1. **Build and start containers:**
   ```bash
   docker-compose -f docker-compose.dev.yml up --build
   ```

2. **Initialize database (in another terminal):**
   ```bash
   docker-compose -f docker-compose.dev.yml exec web flask db init
   docker-compose -f docker-compose.dev.yml exec web flask db migrate -m "Initial migration"
   docker-compose -f docker-compose.dev.yml exec web flask db upgrade
   ```

3. **Access the application:**
   - Open http://localhost:5000 in your browser
   - Register a new account
   - Start using Dram Planner!

### Environment Variables

Create a `.env` file (optional, defaults work for development):

```bash
SECRET_KEY=your-secret-key-here
DB_PASSWORD=your-database-password
FLASK_ENV=development
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
docker-compose -f docker-compose.dev.yml exec web flask db migrate -m "Description"

# Apply migration
docker-compose -f docker-compose.dev.yml exec web flask db upgrade

# Rollback migration
docker-compose -f docker-compose.dev.yml exec web flask db downgrade
```

### View Logs

```bash
# All logs
docker-compose -f docker-compose.dev.yml logs -f

# Web service only
docker-compose -f docker-compose.dev.yml logs -f web
```

### Access Container Shell

```bash
docker-compose -f docker-compose.dev.yml exec web bash
```

### Testing

```bash
# Run tests (when implemented)
docker-compose -f docker-compose.dev.yml exec web pytest
```

## Deployment

### Production Deployment

See [DOCKER.md](DOCKER.md) for comprehensive deployment instructions.

**Quick Start:**
```bash
# Set environment variables
export SECRET_KEY=your-secret-key
export DB_PASSWORD=your-db-password

# Start production stack
docker-compose up -d

# Initialize database
docker-compose exec web flask db upgrade
```

The application uses Docker exclusively for all deployment scenarios.

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

