from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=32, null=True, blank=True)
    password = models.CharField(max_length=32, null=True, blank=True)
    email = models.CharField(max_length=32, null=True, blank=True)
    mybugs = models.CharField(max_length=32, null=True, blank=True)
