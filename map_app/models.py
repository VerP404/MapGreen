from django.db import models
from django.contrib.auth.models import User


class TypeObject(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subtypes')
    color = models.CharField(max_length=7, unique=True)  # Цвет в формате HEX

    def __str__(self):
        return self.name

class Object(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    polygon = models.TextField(blank=True, null=True)
    type_object = models.ForeignKey(TypeObject, on_delete=models.CASCADE)
    photos = models.ImageField(upload_to='photos/', blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.name
