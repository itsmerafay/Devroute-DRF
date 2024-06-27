from django.db import models
from authentication.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    CITY_CHOICES = [
        ('KHI', 'Karachi'),
        ('LHR', 'Lahore'),
        ('ISB', 'Islamabad'),
        ('FSD', 'Faisalabad'),
        ]
    city = models.CharField(max_length=3, choices=CITY_CHOICES)
    cnic = models.CharField(max_length=13, unique=True)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.user.email if self.user else 'UserProfile'
    
    