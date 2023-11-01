from django.db import models

# Create your models here.

class register(models.Model):
    username=models.CharField(max_length=30)
    email=models.EmailField()
    password=models.IntegerField() 
    nid=models.IntegerField() 