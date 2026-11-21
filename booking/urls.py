
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),

    path('show/<int:show_id>/seats/', views.seat_selection, name='seat_selection'),

    path('show/<int:show_id>/book/', views.create_booking, name='create_booking'),

    path('register/', views.register_view, name='register'),

    path('login/', views.login_view, name='login'),

    path('logout/', views.logout_view, name='logout'),

    path('my-bookings/', views.my_bookings, name='my_bookings'),

    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),

    path('booking/<int:booking_id>/ticket/', views.view_ticket, name='view_ticket'),
]
