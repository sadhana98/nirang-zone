from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class NirangUser(AbstractUser):
    mobile = models.CharField(max_length=150, unique=True)
    email = models.CharField(max_length=150, unique=True)
    deleted = models.BooleanField(default=False)
