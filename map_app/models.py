from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, unique=False, default='#0000F')
    auto_publish = models.BooleanField(default=False)  # Поле для автоматической публикации

    def __str__(self):
        return self.name


class TypeObject(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='types')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_published = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.id:  # Only set is_published on new objects
            self.is_published = self.type_object.category.auto_publish
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)
    profession = models.CharField(max_length=50, blank=True)
    workplace = models.CharField(max_length=100, blank=True)
    position = models.CharField(max_length=50, blank=True)
