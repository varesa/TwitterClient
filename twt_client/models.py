from django.db import models

# Create your models here.

class Tweet(models.Model):
    id = models.IntegerField(primary_key=True)
    data = models.CharField(max_length=16384)
