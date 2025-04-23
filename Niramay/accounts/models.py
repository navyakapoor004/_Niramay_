from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

class customuser(AbstractUser):
    email=models.EmailField(unique=True)
    username=models.CharField(unique=True,max_length=100)

class OTP(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    otp_code=models.CharField( max_length=6)
    created_at=models.DateTimeField( auto_now_add=True)

def is_expired(self):
    expiration_time=self.created_at + timedelta(minutes=2)
    return timezone.now()>expiration_time

