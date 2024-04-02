from django.db import models

# Create your models here.
from django.db import models

from datetime import date

class Role(models.Model):
    name = models.CharField(max_length=255)
    clearance = models.IntegerField()
    is_delete= models.IntegerField(default=0)

class User(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email = models.CharField(max_length=255,unique=True)
    password = models.CharField(max_length=255)
    phone = models.CharField(max_length=255, null=True, blank=True)
    occupation = models.CharField(max_length=255)
    instituation = models.CharField(max_length=255)

    creationDate = models.DateField(null=True, blank=True)
    # by default it is 1 which is soft delete, 1 means requires approval and 2 is ok
    approve = models.IntegerField(null=True, blank=True, default=0)
    role = models.ForeignKey(Role, on_delete=models.CASCADE,default=3)
    is_delete= models.IntegerField(default=0)

class Data_type(models.Model):
    name = models.CharField(max_length=255)
    code= models.CharField(max_length=3,null=True, blank=True, default=0)
    is_delete= models.IntegerField(default=0)

class Basic_data(models.Model):
    details = models.TextField(null=True, blank=True)
    code =  models.CharField(max_length=9)
    references=models.TextField(null=True, blank=True)
    funding = models.TextField(null=True,blank=True)
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    type=models.ForeignKey(Data_type, on_delete=models.CASCADE,null=True,blank=True)
    approved = models.IntegerField(null=True, blank=True,default=0)
    attachment = models.FileField(null=True, blank=True)
    creationDate = models.DateField(null=True, blank=True,default=date.today)
    is_delete= models.IntegerField(default=0)

class File_data(models.Model):
    basic_data_id = models.ForeignKey(Basic_data, on_delete=models.CASCADE,null=True,blank=True)
    attachment = models.FileField(null=True, blank=True)
    is_delete= models.IntegerField(default=0)
class column_data(models.Model):
    file_data_id = models.ForeignKey(File_data, on_delete=models.CASCADE, null=True, blank=True)
    col_index = models.IntegerField(null=True, blank=True,default=0)
    sheet_index = models.IntegerField(null=True, blank=True,default=0)
    column_names = models.TextField(null=True, blank=True, default=0)
    is_delete= models.IntegerField(default=0)




