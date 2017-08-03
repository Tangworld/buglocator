from django.db import models

# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=32, null=True, blank=True)
    password = models.CharField(max_length=32, null=True, blank=True)
    email = models.CharField(max_length=32, null=True, blank=True)
    mybugs = models.CharField(max_length=32, null=True, blank=True)
    avatarloc = models.CharField(max_length=32, null=True, blank=True)
    isadmin = models.CharField(max_length=32, null=True, blank= True)


class Report(models.Model):
    bugid = models.CharField(max_length=20, null=True, blank=True)
    summary = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(max_length=700, null=True, blank=True)
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

class Record(models.Model):
    b1 = models.CharField(max_length=20, null=True, blank=True)
    b2 = models.CharField(max_length=20, null=True, blank=True)
    b3 = models.CharField(max_length=20, null=True, blank=True)
    b4 = models.CharField(max_length=20, null=True, blank=True)
    b5 = models.CharField(max_length=20, null=True, blank=True)
    b6 = models.CharField(max_length=20, null=True, blank=True)
    b7 = models.CharField(max_length=20, null=True, blank=True)
    b8 = models.CharField(max_length=20, null=True, blank=True)
    b9 = models.CharField(max_length=20, null=True, blank=True)
    b10 = models.CharField(max_length=20, null=True, blank=True)
    b11 = models.CharField(max_length=20, null=True, blank=True)
    b12 = models.CharField(max_length=20, null=True, blank=True)

    f1 = models.CharField(max_length=20, null=True, blank=True)
    f2 = models.CharField(max_length=20, null=True, blank=True)
    f3 = models.CharField(max_length=20, null=True, blank=True)
    f4 = models.CharField(max_length=20, null=True, blank=True)
    f5 = models.CharField(max_length=20, null=True, blank=True)
    f6 = models.CharField(max_length=20, null=True, blank=True)
    f7 = models.CharField(max_length=20, null=True, blank=True)
    f8 = models.CharField(max_length=20, null=True, blank=True)
    f9 = models.CharField(max_length=20, null=True, blank=True)
    f10 = models.CharField(max_length=20, null=True, blank=True)
    f11 = models.CharField(max_length=20, null=True, blank=True)
    f12 = models.CharField(max_length=20, null=True, blank=True)


    year = models.CharField(max_length=20, null=True, blank=True)
    userid = models.CharField(max_length=20, null=True, blank=True)


class bugidmap(models.Model):
    bugidnumber = models.CharField(max_length=20, null=True, blank=True)
    bugid = models.CharField(max_length=20, null=True, blank=True)


class filemap(models.Model):
    filenumber = models.CharField(max_length=20, null=True, blank=True)
    filepath = models.CharField(max_length=200, null=True, blank=True)


class reports(models.Model):
    reportnumber = models.CharField(max_length=20, null=True, blank=True)
    content = models.TextField(max_length=500, null=True, blank=True)


class f2w(models.Model):
    fileID = models.CharField(max_length=20, null=True, blank=True)
    keywords = models.TextField(max_length=200, null=True, blank=True)

class wordmap(models.Model):
    wordID = models.CharField(max_length=20, null=True, blank=True)
    word = models.TextField(max_length=500, null=True, blank=True)