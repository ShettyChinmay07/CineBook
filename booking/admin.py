
from django.contrib import admin
from .models import Movie, Theatre, Show, Booking, BookedSeat


# MOVIE ADMIN
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'genre',
        'language',
        'duration',
        'is_active'
    )

    search_fields = ('title', 'genre', 'language')

    list_filter = ('genre', 'language', 'is_active')

    list_editable = ('is_active',)

    ordering = ('title',)


# THEATRE ADMIN
@admin.register(Theatre)
class TheatreAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'location',
        'city'
    )

    search_fields = ('name', 'location', 'city')

    list_filter = ('city', 'location')


# SHOW ADMIN
@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    list_display = (
        'movie',
        'theatre',
        'show_date',
        'show_time',
        'ticket_price',
        'available_seats',
        'is_active'
    )

    search_fields = (
        'movie__title',
        'theatre__name'
    )

    list_filter = (
        'show_date',
        'theatre',
        'is_active'
    )

    ordering = ('show_date', 'show_time')


# BOOKED SEAT INLINE
class BookedSeatInline(admin.TabularInline):
    model = BookedSeat
    extra = 0
    can_delete = False
    readonly_fields = ('show', 'seat_number')


# BOOKING ADMIN
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):

    list_display = (
        'booking_reference',
        'customer_name',
        'customer_email',
        'show',
        'total_amount',
        'status',
        'created_at'
    )

    search_fields = (
        'customer_name',
        'customer_email',
        'booking_reference'
    )

    list_filter = (
        'status',
        'created_at'
    )

    readonly_fields = (
        'booking_reference',
        'status',
        'created_at'
    )

    date_hierarchy = 'created_at'

    inlines = [BookedSeatInline]

    ordering = ('-created_at',)


# BOOKED SEAT ADMIN
@admin.register(BookedSeat)
class BookedSeatAdmin(admin.ModelAdmin):

    list_display = (
        'booking',
        'show',
        'seat_number'
    )

    list_filter = ('show',)

    search_fields = (
        'seat_number',
        'booking__customer_name'
    )
# CINEBOOK ADMIN BRANDING

admin.site.site_header = "CineBook Administration"
admin.site.site_title = "CineBook Admin Portal"
admin.site.index_title = "Welcome to CineBook Management"