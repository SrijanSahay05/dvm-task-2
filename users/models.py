from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    USER_TYPE_CHOICES = (
        ("passenger", "Passenger"),
        ("railwaystaff", "Railway Staff"),
        ("admin", "Admin"),
    )
    user_type = models.CharField(
        max_length=20, choices=USER_TYPE_CHOICES, default="passenger"
    )


class PassengerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)


class RailwayStaffProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
