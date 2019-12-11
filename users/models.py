from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import gettext as _


class CustomUser(AbstractUser):
    USERNAME_FIELD = 'email'
    email = models.EmailField(_('email address'), unique=True)
    contact = models.CharField(max_length=12)
    address = models.CharField(max_length=1024)
    pincode = models.IntegerField(null=True)

    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
