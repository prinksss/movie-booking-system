from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Booking,CustomUser,Movie

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

class UserLoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['movie', 'booking_type', 'seat_count']
