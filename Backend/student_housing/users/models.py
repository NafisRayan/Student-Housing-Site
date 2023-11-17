from django.db import models

# Create your models here.

class Register(models.Model):
    username=models.CharField(max_length=30)
    email=models.EmailField()
    password=models.CharField(max_length=100) 
    nid=models.IntegerField() 

class DormRooms(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    popularity = models.CharField(max_length=20)
    type = models.CharField(max_length=50)
    price = models.CharField(max_length=20)
    link = models.URLField(max_length=200)