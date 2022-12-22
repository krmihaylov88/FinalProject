from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)

    def __str__(self):
        return f'Profile for user {self.user.username}'


class AccountData(models.Model):
    username = models.CharField(max_length=30)
    key = models.CharField(max_length=30)
    value = models.CharField(max_length=300, null=True, blank=True)

    class Meta:
        unique_together = ('username', 'key')
