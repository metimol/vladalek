from django.db import models
from django.contrib.auth.models import AbstractUser

class Profile(AbstractUser):
	code = models.TextField(blank=True, null=True, verbose_name='Код')
	avatar = models.URLField(blank=True, null=True, verbose_name="Аватар")
	email = models.EmailField(verbose_name='Почта', unique=True)
	github = models.URLField(verbose_name='Ссылка на GitHub', blank=True, null=True)
	instagram = models.URLField(verbose_name='Ссылка на Instagram', blank=True, null=True)
	facebook = models.URLField(verbose_name='Ссылка на Facebook', blank=True, null=True)
