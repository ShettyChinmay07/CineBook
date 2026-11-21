
import base64
from io import BytesIO

import qrcode

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django.shortcuts import render, get_object_or_404, redirect
from django.db import transaction, IntegrityError
from django.views.decorators.http import require_POST
from django.urls import reverse

from .models import Movie, Show, Booking, BookedSeat


# GENERATE TICKET QR CODE
def generate_ticket_qr(request, booking):

    ticket_url = request.build_absolute_uri(
        reverse('view_ticket', args=[booking.id])
    )

    qr = qrcode.QRCode(
        version=1,
        box_size=6,
        border=3
    )

    qr.add_data(ticket_url)
    qr.make(fit=True)

    qr_image = qr.make_image(
        fill_color="black",
        back_color="white"
    )

    buffer = BytesIO()

    qr_image.save(buffer, format='PNG')

    qr_code = base64.b64encode(
        buffer.getvalue()
    ).decode('utf-8')

    return qr_code


# HOME PAGE
@login_required(login_url='login')
def home(request):

    search_query = request.GET.get('q', '').strip()

    movies = Movie.objects.filter(is_active=True)

    if search_query:
        movies = movies.filter(title__icontains=search_query)

    user_booking_count = Booking.objects.filter(
        user=request.user
    ).count()

    return render(request, 'booking/home.html', {
        'movies': movies,
        'search_query': search_query,
        'user_booking_count': user_booking_count
    })


# MOVIE DETAILS
@login_required(login_url='login')
def movie_detail(request, movie_id):

    movie = get_object_or_404(
        Movie,
        id=movie_id,
        is_active=True
    )

    shows = Show.objects.filter(
        movie=movie,
        is_active=True
    ).select_related('theatre').order_by(
        'show_date', 'show_time'
    )

    return render(request, 'booking/movie_detail.html', {
        'movie': movie,
        'shows': shows
    })


# SEAT SELECTION
@login_required(login_url='login')
def seat_selection(request, show_id):

    show = get_object_or_404(
        Show,
        id=show_id,
        is_active=True
    )

    return render_seat_selection(request, show)


def render_seat_selection(request, show, error=None):

    booked_seats = list(
        BookedSeat.objects.filter(
            show=show
        ).values_list('seat_number', flat=True)
    )

    return render(request, 'booking/seat_selection.html', {
        'show': show,
        'booked_seats': booked_seats,
        'error': error
    })


# CREATE BOOKING
@login_required(login_url='login')
def create_booking(request, show_id):

    show = get_object_or_404(
        Show,
        id=show_id,
        is_active=True
    )

    if request.method != 'POST':
        return redirect('seat_selection', show_id=show.id)

    customer_name = request.POST.get(
        'customer_name', ''
    ).strip()

    customer_email = request.POST.get(
        'customer_email', ''
    ).strip()

    seat_input = request.POST.get('selected_seats', '')

    selected_seats = list(dict.fromkeys(
        seat.strip()
        for seat in seat_input.split(',')
        if seat.strip()
    ))

    valid_seats = {
        f'{row}{number}'
        for row in ['A', 'B', 'C', 'D', 'E']
        for number in range(1, 11)
    }

    if not customer_name or not customer_email or not selected_seats:

        return render_seat_selection(
            request,
            show,
            'Please enter your details and select at least one seat.'
        )

    if not all(seat in valid_seats for seat in selected_seats):

        return render_seat_selection(
            request,
            show,
            'Invalid seat selection.'
        )

    try:

        with transaction.atomic():

            show = Show.objects.select_for_update().get(
                id=show_id,
                is_active=True
            )

            already_booked = BookedSeat.objects.filter(
                show=show,
                seat_number__in=selected_seats
            ).exists()

            if already_booked:

                raise ValueError(
                    'One or more selected seats are already booked. '
                    'Please select different seats.'
                )

            if len(selected_seats) > show.available_seats:

                raise ValueError('Not enough seats are available.')

            # CREATE BOOKING AND SAVE SEAT NUMBERS
            booking = Booking.objects.create(
                user=request.user,
                show=show,
                customer_name=customer_name,
                customer_email=customer_email,
                total_amount=show.ticket_price * len(selected_seats),
                seat_numbers=', '.join(selected_seats)
            )

            # SAVE BOOKED SEATS
            BookedSeat.objects.bulk_create([
                BookedSeat(
                    booking=booking,
                    show=show,
                    seat_number=seat
                )
                for seat in selected_seats
            ])

            # UPDATE AVAILABLE SEATS
            show.available_seats -= len(selected_seats)

            show.save(update_fields=['available_seats'])

        # GENERATE QR CODE
        qr_code = generate_ticket_qr(request, booking)

        return render(
            request,
            'booking/booking_confirmation.html',
            {
                'booking': booking,
                'qr_code': qr_code
            }
        )

    except IntegrityError:

        return render_seat_selection(
            request,
            show,
            'One or more selected seats are already booked. Please try again.'
        )

    except ValueError as error:

        return render_seat_selection(
            request,
            show,
            str(error)
        )


# USER REGISTRATION
def register_view(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':

        form = UserCreationForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            return redirect('home')

    else:

        form = UserCreationForm()

    return render(request, 'booking/register.html', {
        'form': form
    })


# USER LOGIN
def login_view(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':

        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():

            user = form.get_user()

            login(request, user)

            return redirect('home')

    else:

        form = AuthenticationForm(request)

    return render(request, 'booking/login.html', {
        'form': form
    })


# USER LOGOUT
def logout_view(request):

    if request.method == 'POST':

        logout(request)

    return redirect('home')


# MY BOOKINGS
@login_required(login_url='login')
def my_bookings(request):

    bookings = Booking.objects.filter(
        user=request.user
    ).select_related(
        'show__movie',
        'show__theatre'
    ).prefetch_related(
        'booked_seats'
    ).order_by('-created_at')

    return render(request, 'booking/my_bookings.html', {
        'bookings': bookings
    })


# CANCEL BOOKING
@login_required(login_url='login')
@require_POST
def cancel_booking(request, booking_id):

    with transaction.atomic():

        booking = get_object_or_404(
            Booking.objects.select_for_update(),
            id=booking_id,
            user=request.user
        )

        if booking.status == 'Confirmed':

            show = Show.objects.select_for_update().get(
                id=booking.show_id
            )

            # GET ORIGINAL BOOKED SEAT NUMBERS
            booked_seat_numbers = list(
                booking.booked_seats.order_by(
                    'seat_number'
                ).values_list(
                    'seat_number',
                    flat=True
                )
            )

            # PRESERVE SEAT NUMBERS
            if not booking.seat_numbers:

                booking.seat_numbers = ', '.join(
                    booked_seat_numbers
                )

                booking.save(
                    update_fields=['seat_numbers']
                )

            # RELEASE BOOKED SEATS
            booking.booked_seats.all().delete()

            # RESTORE AVAILABLE SEATS
            show.available_seats += len(booked_seat_numbers)

            show.save(
                update_fields=['available_seats']
            )

            # UPDATE BOOKING STATUS
            booking.status = 'Cancelled'

            booking.save(
                update_fields=['status']
            )

    return redirect('my_bookings')


# VIEW / REPRINT BOOKING TICKET
@login_required(login_url='login')
def view_ticket(request, booking_id):

    booking = get_object_or_404(
        Booking.objects.select_related(
            'show__movie',
            'show__theatre'
        ).prefetch_related(
            'booked_seats'
        ),
        id=booking_id,
        user=request.user,
        status='Confirmed'
    )

    # GENERATE QR CODE AGAIN WHEN REPRINTING
    qr_code = generate_ticket_qr(request, booking)

    return render(
        request,
        'booking/booking_confirmation.html',
        {
            'booking': booking,
            'qr_code': qr_code
        }
    )
