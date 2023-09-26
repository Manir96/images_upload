from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Product(models.Model):
    name = models.CharField()
    product_image = models.ImageField()

    def __str__(self):
        return str(self.id)
