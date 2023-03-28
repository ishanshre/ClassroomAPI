from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField

from rest_framework_simplejwt.tokens import RefreshToken
# Create your models here.

class User(AbstractUser):
    email = models.EmailField(_("Email Address"),max_length=255, unique=True)

    def get_tokens(self):
        refresh = RefreshToken.for_user(self)
        tokens = {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }
        return tokens


class Profile(models.Model):
    class GENDER(models.TextChoices):
        MALE = "M", "Male"
        FEMALE = "F", "Female"
        OTHERS = "O", "Others"
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    profile_pic = models.ImageField(upload_to="user/profile/pic/", default="default/profile.jpeg")
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER.choices, null=True, blank=True)
    phone = PhoneNumberField(null=True, blank=True)
    address = models.CharField(max_length=500, null=True, blank=True)
    bio = models.TextField(max_length=10000, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"
    