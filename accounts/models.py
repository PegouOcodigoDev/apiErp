from django.db import models
from django.contrib.auth.models import AbstractBaseUser,Permission


class User(AbstractBaseUser):
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    is_owner = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email
    
class Group(models.Model):
    name = models.CharField(max_length=85)
    enterprie = models.ForeignKey('companies.Enterprise', on_delete=models.CASCADE)

