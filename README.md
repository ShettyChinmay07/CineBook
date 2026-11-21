
# CineBook - Movie Ticket Booking System

## Project Overview

CineBook is a web-based movie ticket booking system developed using Python and Django.

It allows users to browse movies, view available shows, select seats, book movie tickets, cancel bookings and access digital tickets.

## Technologies Used

- Python
- Django
- HTML
- CSS
- JavaScript
- SQLite Database
- Pillow
- QR Code

## Main Features

1. User Registration and Login
2. Movie Listing and Search
3. Movie Details and Show Information
4. Theatre and Show Management
5. Interactive Seat Selection
6. Prevention of Double Seat Booking
7. Online Ticket Booking
8. Booking Confirmation
9. My Bookings
10. Booking Cancellation
11. Automatic Seat Release
12. Booking History
13. Digital Ticket Generation
14. QR Code Generation
15. Printable Movie Tickets
16. Django Admin Management

## Installation

### 1. Create a Virtual Environment

```bash
python -m venv venv
```

### 2. Activate Virtual Environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply Database Migrations

```bash
python manage.py migrate
```

### 5. Run the Development Server

```bash
python manage.py runserver
```

### 6. Open the Website

```text
http://127.0.0.1:8000/
```

## Admin Panel

Open:

```text
http://127.0.0.1:8000/admin/
```

## Database

CineBook uses SQLite for storing:

- Movies
- Theatres
- Shows
- User information
- Bookings
- Booked seats

## Project Structure

- booking/ - Django application
- cinebook/ - Django project configuration
- templates/ - HTML templates
- static/ - CSS and static files
- media/ - Movie poster images
- db.sqlite3 - SQLite database
- manage.py - Django management file
- requirements.txt - Project dependencies

## Conclusion

CineBook provides a convenient platform for movie ticket booking with seat management, booking cancellation, digital tickets and QR code generation.
