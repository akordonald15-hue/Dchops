from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField  # import CloudinaryField

class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    avatar = CloudinaryField('avatar', blank=True, null=True)  # corrected

    def __str__(self):
        return f"{self.user.username}'s profile"
