from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.deconstruct import deconstructible
from ckeditor.fields import RichTextField


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = RichTextField(blank=True)
    color = models.CharField(max_length=7, unique=False, default='#0000FF')
    icon = models.CharField(max_length=50, default='ri-file-list-line')

    def __str__(self):
        return self.name


class TypeObject(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='types')
    name = models.CharField(max_length=255)
    description = RichTextField(blank=True)
    color = models.CharField(max_length=7, unique=True)

    def __str__(self):
        return self.name


class Object(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    polygon = models.TextField(blank=True, null=True)
    type_object = models.ForeignKey(TypeObject, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_published = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=timezone.now)
    date_published = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.is_published = self.user.auto_publish
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


@deconstructible
class PathAndRename:
    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        return f'projects/{instance.object.id}/{filename}'


def get_upload_path(instance, filename):
    return f'projects/{instance.object.id}/{filename}'


class Photo(models.Model):
    object = models.ForeignKey(Object, related_name='photos', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_upload_path)
    description = models.TextField(blank=True)
    is_main = models.BooleanField(default=False)

    def __str__(self):
        return f'Photo for {self.object.name}'


class Link(models.Model):
    object = models.ForeignKey(Object, related_name='links', on_delete=models.CASCADE)
    url = models.URLField()
    description = models.TextField()

    def __str__(self):
        return self.url


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    first_name = models.CharField(_('Имя'), max_length=30, blank=True)
    last_name = models.CharField(_('Фамилия'), max_length=30, blank=True)
    email = models.EmailField(_('Электронная почта'), unique=True)
    phone = models.CharField(_('Телефон'), max_length=15, blank=True)
    profession = models.CharField(_('Профессия'), max_length=50, blank=True)
    workplace = models.CharField(_('Место работы'), max_length=100, blank=True)
    position = models.CharField(_('Должность'), max_length=50, blank=True)
    auto_publish = models.BooleanField(default=False, verbose_name="Автопубликация")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class AboutPage(models.Model):
    content = RichTextField(blank=True)

    def __str__(self):
        return "О нас"
