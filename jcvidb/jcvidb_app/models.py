from django.db import models

# Create your models here.
from django.db import models


class Role(models.Model):
    name = models.CharField(max_length=255)
    clearance = models.IntegerField()


class User(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    phone = models.CharField(max_length=255, null=True, blank=True)
    occupation = models.CharField(max_length=255)
    instituation = models.CharField(max_length=255)

    creationDate = models.DateField(null=True, blank=True)
    # by default it is 1 which is soft delete, 1 means requires approval and 2 is ok
    approve = models.IntegerField(null=True, blank=True, default=0)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)


class Proteomic(models.Model):
    freeGeneSet = models.CharField(max_length=255)
    PGAN = models.CharField(max_length=255, null=True, blank=True)
    locusTag = models.CharField(max_length=255, null=True, blank=True)

    createdBy = models.ForeignKey(User, on_delete=models.CASCADE)
    essentiality = models.CharField(max_length=255)
    transporters = models.CharField(max_length=255, null=True, blank=True)
    coverage = models.IntegerField(null=True, blank=True)

    attachment = models.FileField(null=True, blank=True)
    originalName = models.CharField(max_length=255, null=True, blank=True)
    creationDate = models.DateField(null=True, blank=True)
