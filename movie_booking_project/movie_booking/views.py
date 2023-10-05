from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .models import Movie, Booking
from django.db import models
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm,UserLoginForm,BookingForm
from django.views.generic import ListView, CreateView

# User Registration View
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('movie_list') 
        else:
            print(form.errors)
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('movie_list')  # Redirect to your desired page after login
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required
def profile(request):
    user = request.user
    return render(request, 'movie_booking/profile.html', {'user': user})

class MovieListView(ListView):
    model = Movie
    template_name = 'movie_booking/movie_list.html'
    context_object_name = 'movies'

# @login_required
# def book_movie(request, movie_id):
#     movie = Movie.objects.get(id=movie_id)
#     if request.method == 'POST':
#         form = BookingForm(request.POST)
#         if form.is_valid():
#             booking_type = form.cleaned_data['booking_type']
#             ticket_count = form.cleaned_data['ticket_count']
#             seat_count = form.cleaned_data['seat_count'] 

#             if booking_type == 'single':
#                 if movie.seats_available >= seat_count:
#                         booking = Booking(user=request.user, movie=movie, booking_type=booking_type, seat_count=seat_count)
#                         booking.save()
#                         movie.seats_available -= seat_count
#                         movie.save()
#                         messages.success(request, 'Booking successful!')
#                         print("&&&&&&&&&&&&&")
#                 else:
#                         messages.error(request, 'Not enough available seats for single booking.')
            
#             elif booking_type == 'multiple':
#                 if movie.seats_available >= seat_count * 2:
#                     booking = Booking(user=request.user, movie=movie, booking_type=booking_type, ticket_count=ticket_count)
#                     booking.save()
#                     movie.seats_available -= ticket_count * 2
#                     movie.save()
#                     messages.success(request, 'Booking successful!')
#                     print("%%%%%%%%%%%%%%%%%%%%%%%%")
#                 else:
#                     messages.error(request, 'Not enough available seats for multiple booking.')
#             else:
#                 messages.error(request, 'Invalid booking type.')
#                 print("*******************************")
#             return redirect('movie_list')
#         else:
#             messages.error(request, 'Invalid form data. Please check your input.')
#             print(form.errors)
#             print(request.POST)
#     else:
#         form = BookingForm()
#     return render(request, 'movie_booking/book_movie.html', {'movie': movie})
@login_required
def book_movie(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    if request.method == 'POST':
        booking_type = request.POST.get('booking_type')
        seat_count = int(request.POST.get('seat_count', 0))  # Default to 0 if not provided
        print("7777777777777777777777777")
        if booking_type in ['single', 'multiple']:
            if booking_type == 'single':
                if movie.seats_available >= seat_count:
                    booking = Booking(user=request.user, movie=movie, booking_type=booking_type, seat_count=seat_count)
                    booking.save()
                    movie.seats_available -= seat_count
                    movie.save()
                    messages.success(request, 'Booking successful!')
                    print("&&&&&&&&&&&&&")
                else:
                    messages.error(request, 'Not enough available seats for single booking.')
            elif booking_type == 'multiple':
                if movie.seats_available >= seat_count * 2:
                    booking = Booking(user=request.user, movie=movie, booking_type=booking_type, seat_count=seat_count)
                    booking.save()
                    movie.seats_available -= seat_count * 2
                    movie.save()
                    messages.success(request, 'Booking successful!')
                    print("%%%%%%%%%%%%%%%%%%%%%%%%")
                else:
                    messages.error(request, 'Not enough available seats for multiple booking.')
        else:
            messages.error(request, 'Invalid booking type.')
            print("*******************************")
        return redirect('movie_list')
    else:
        form = BookingForm()  # You can still use a form to display the booking options
    return render(request, 'movie_booking/book_movie.html', {'movie': movie})



def create_booking(request, movie, booking_type, seat_count):
    booking = Booking(user=request.user, movie=movie, booking_type=booking_type, seat_count=seat_count)
    booking.save()
    if booking_type == 'single':
        movie.seats_available -= seat_count
    elif booking_type == 'multiple':
        movie.seats_available -= seat_count * 2
    movie.save()
    messages.success(request, 'Booking successful!')

@login_required
def my_bookings(request):
    user = request.user
    bookings = Booking.objects.filter(user=user)
    return render(request, 'movie_booking/my_bookings.html', {'bookings': bookings})

def movie_seats(request, movie_id):
    movie = Movie.objects.get(pk=movie_id)
    booked_seats = Booking.objects.filter(movie=movie).aggregate(total_booked_seats=models.Sum('seat_count'))['total_booked_seats'] or 0
    available_seats = movie.total_seats - booked_seats

    return render(request, 'movie_booking/movie_seats.html', {'movie': movie, 'available_seats': available_seats, 'booked_seats': booked_seats})