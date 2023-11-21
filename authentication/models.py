from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator

USER_ROLES = [("Student", "Student"), ("Moderator", "Moderator")]


class User(AbstractUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(unique=True, max_length=13, validators=[MinLengthValidator(11)])
    national_id = models.CharField(max_length=10, validators=[MinLengthValidator(10)])
    role = models.CharField(choices=USER_ROLES, max_length=15)
