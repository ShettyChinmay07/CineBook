
# CineBook - Movie Ticket Booking System

CineBook is a web-based movie ticket booking application developed using Python and Django.

## Features

- User registration and login
- Movie browsing and search
- Movie details and show listings
- Theatre management
- Interactive seat selection
- Prevention of double booking
- Ticket booking and confirmation
- Booking cancellation
- Automatic seat release
- My Bookings and booking history
- Digital tickets
- QR code generation
- Printable movie tickets
- Django Admin Panel

## Technologies Used

- Python
- Django
- HTML
- CSS
- JavaScript
- SQLite
- PostgreSQL
- Pillow
- QR Code

## Installation

1. Create a virtual environment:

   `python -m venv venv`

2. Activate it:

   `.\venv\Scripts\Activate`

3. Install dependencies:

   `pip install -r requirements.txt`

4. Apply migrations:

   `python manage.py migrate`

5. Start the server:

   `python manage.py runserver`

6. Open `http://127.0.0.1:8000/`

## Project Structure

- booking/ - Main Django application
- cinebook/ - Django configuration
- templates/ - HTML pages
- static/ - CSS and static files
- media/ - Movie posters
- requirements.txt - Dependencies
- build.sh - Deployment build script

## Author

Chinmay Shetty
