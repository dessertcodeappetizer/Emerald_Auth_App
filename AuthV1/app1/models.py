from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User_auth(AbstractUser):
    first_name = models.CharField(max_length=50, null=False, blank=False)
    last_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    phone = models.CharField(max_length=14, null=False, blank=False)
    gender = models.CharField(max_length=7, null=False, blank=False)
    password = models.CharField(max_length=256, null=False, blank=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []