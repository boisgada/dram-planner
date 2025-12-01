# Archived Files

This directory contains files that were used for direct Python execution but have been archived in favor of Docker-only deployment.

## Files

- `run.py` - Direct Python execution script (replaced by Docker)

## Why Archived?

The web application now uses Docker exclusively for:
- Consistent environments across development and production
- Easier deployment
- Better isolation
- Simplified dependency management

## To Run the Application

Use Docker Compose instead:

```bash
# Development
docker-compose -f docker-compose.dev.yml up

# Production
docker-compose up
```

See the main [README.md](../README.md) and [DOCKER.md](../DOCKER.md) for details.

