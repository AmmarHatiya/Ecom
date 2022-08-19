from signal import default_int_handler
from django.db import models

# Create your models here.

class Products(models.Model):
    ProductID = models.AutoField(primary_key=True)
    ProductName = models.CharField(max_length=200)
    ProductDescription = models.CharField(max_length=500)
    Price = models.CharField(max_length=20)
    PhotoFileName = models.CharField(max_length=200)