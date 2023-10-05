from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Movie, Booking
from django.db import models

# Register your models here.
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'email', 'first_name', 'last_name')

admin.site.register(CustomUser, CustomUserAdmin)

def view_users_booked_for_movie(modeladmin, request, queryset):
    if queryset.count() == 1:
        movie = queryset.first()
        bookings = Booking.objects.filter(movie=movie)
        users = [booking.user for booking in bookings]
        users = set(users) 
        users_list = ", ".join([user.username for user in users])
        message = f"Users who have booked tickets for '{movie.title}': {users_list}"
        modeladmin.message_user(request, message)
    else:
        modeladmin.message_user(request, "Please select a single movie to view users.")

view_users_booked_for_movie.short_description = "View Users Booked for Movie"


def seats_status_for_movie(modeladmin, request, queryset):
    if queryset.count() == 1:
        movie = queryset.first()
        total_seats = movie.total_seats
        booked_seats = Booking.objects.filter(movie=movie).aggregate(total_booked_seats=models.Sum('seat_count'))['total_booked_seats'] or 0
        pending_seats = total_seats - booked_seats

        message = f"Movie: {movie.title}\nTotal Seats: {total_seats}\nBooked Seats: {booked_seats}\nPending Seats: {pending_seats}"
        modeladmin.message_user(request, message)
    else:
        modeladmin.message_user(request, "Please select a single movie to view seats status.")

seats_status_for_movie.short_description = "View Seats Status for Movie"

class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date') 
    actions = [view_users_booked_for_movie,seats_status_for_movie]

admin.site.register(Movie, MovieAdmin)
admin.site.register(Booking)