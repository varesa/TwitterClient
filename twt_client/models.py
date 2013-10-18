from django.db import models
from django.contrib import admin

# Create your models here.

class Tweet(models.Model):
    id = models.IntegerField(primary_key=True)
    data = models.CharField(max_length=16384)

admin.site.register(Tweet)

class Meta(models.Model):
    id = models.IntegerField(primary_key=True)
    time = models.IntegerField()