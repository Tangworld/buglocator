from django.db import models

# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=32, null=True, blank=True)
    password = models.CharField(max_length=32, null=True, blank=True)
    email = models.CharField(max_length=32, null=True, blank=True)
    mybugs = models.CharField(max_length=32, null=True, blank=True)
    isadmin = models.CharField(max_length=32, null=True, blank= True)


class Report(models.Model):
    bugid = models.CharField(max_length=20, null=True, blank=True)
    summary = models.CharField(max_length=50, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    reporter = models.CharField(max_length=32, null=True, blank=True)
    assignee = models.CharField(max_length=32, null=True, blank=True)
    productid = models.CharField(max_length=32, null=True, blank=True)
    status = models.CharField(max_length=32, null=True, blank=True)
    opendate = models.CharField(max_length=32, null=True, blank=True)
    fixdate = models.CharField(max_length=32, null=True, blank=True)
    method = models.CharField(max_length=32, null=True, blank=True)
    fileloc = models.CharField(max_length=100, null=True, blank=True)
    component = models.CharField(max_length=32, null=True, blank=True)
    version = models.CharField(max_length=32, null=True, blank=True)
    platform = models.CharField(max_length=32, null=True, blank=True)
    os = models.CharField(max_length=32, null=True, blank=True)
    priority = models.CharField(max_length=32, null=True, blank=True)
    severity = models.CharField(max_length=32, null=True, blank=True)
    keywords = models.CharField(max_length=200, null=True, blank=True)


class Product(models.Model):
    name = models.CharField(max_length=32, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)


class ProUser(models.Model):
    product_id = models.CharField(max_length=32)
    user_id = models.CharField(max_length=32)
