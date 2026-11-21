
import uuid

from django.db import models
from django.contrib.auth.models import User


# MOVIE MODEL
class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    genre = models.CharField(max_length=100)
    language = models.CharField(max_length=50)
    duration = models.PositiveIntegerField(help_text='Duration in minutes')
    release_date = models.DateField(null=True, blank=True)
    poster = models.ImageField(upload_to='movie_posters/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


# THEATRE MODEL
class Theatre(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.name


# SHOW MODEL
class Show(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    theatre = models.ForeignKey(Theatre, on_delete=models.CASCADE)
    show_date = models.DateField()
    show_time = models.TimeField()
    ticket_price = models.DecimalField(max_digits=8, decimal_places=2)
    available_seats = models.PositiveIntegerField(default=50)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.movie.title} - {self.show_date} - {self.show_time}"


# BOOKING MODEL
class Booking(models.Model):

    BOOKING_STATUS = [
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='bookings',
        null=True,
        blank=True
    )

    booking_reference = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )

    show = models.ForeignKey(
        Show,
        on_delete=models.PROTECT
    )

    customer_name = models.CharField(max_length=150)
    customer_email = models.EmailField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    # STORE ORIGINAL SEAT NUMBERS
    seat_numbers = models.TextField(
        blank=True,
        default=''
    )

    status = models.CharField(
        max_length=20,
        choices=BOOKING_STATUS,
        default='Confirmed'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer_name} - {self.booking_reference}"


# BOOKED SEAT MODEL
class BookedSeat(models.Model):

    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name='booked_seats'
    )

    show = models.ForeignKey(
        Show,
        on_delete=models.PROTECT
    )

    seat_number = models.CharField(max_length=5)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['show', 'seat_number'],
                name='unique_show_seat'
            )
        ]

    def __str__(self):
        return f"{self.show} - {self.seat_number}"
