from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def __str__(self):
        return self.username

class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    total_seats = models.PositiveIntegerField(default=100)
    release_date = models.DateField()
    seats_available = models.PositiveIntegerField()
    seats_booked = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

class Booking(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    booking_type = models.CharField(max_length=10)  # 'single' or 'multiple'
    seat_count = models.PositiveIntegerField(default=100)
    ticket_count = models.PositiveIntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.movie.title} ({self.booking_type})"
