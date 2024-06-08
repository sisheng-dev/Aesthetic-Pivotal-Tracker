#!/bin/bash

# Wait for the database to be ready
while ! nc -z db 5432; do
  echo "Waiting for PostgreSQL..."
  sleep 1
done

# Run migrations
flask db upgrade

# Start the application
exec "$@"
