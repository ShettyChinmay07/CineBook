
#!/usr/bin/env bash

# Stop deployment if any command fails
set -o errexit

# Install project dependencies
pip install -r requirements.txt

# Prepare static files (CSS, JavaScript and images)
python manage.py collectstatic --no-input

# Apply database migrations
python manage.py migrate
