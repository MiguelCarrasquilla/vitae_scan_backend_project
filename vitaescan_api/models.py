from django.db import models

# Create your models here.

class User(models.Model):
    fullname = models.CharField(max_length=100)
    email = models.CharField(max_length=254)
    id_number = models.IntegerField()
    role = models. CharField(max_length=20)
    status = models. CharField(max_length=20)
