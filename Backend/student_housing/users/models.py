from django.db import models

# Create your models here.

class Register(models.Model):
    username=models.CharField(max_length=30)
    email=models.EmailField()
    password=models.CharField(max_length=100) 
    nid=models.IntegerField() 

    