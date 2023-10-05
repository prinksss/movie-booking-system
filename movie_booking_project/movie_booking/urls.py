from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views

urlpatterns = [
    path('', views.MovieListView.as_view(), name='movie_list'),
    path('movies/<int:movie_id>/book/', views.book_movie, name='book_movie'),
    path('my_bookings/', views.my_bookings, name='my_bookings'),
    path('movies/<int:movie_id>/seats/', views.movie_seats, name='movie_seats'),
    path('signup/', views.register, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'), 
    path('profile/', views.profile, name='profile'),
]
