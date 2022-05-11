from django.db import models
from django.contrib.auth.models import AbstractUser

class Profile(AbstractUser):
	code = models.TextField(blank=True, null=True, verbose_name='Код')
	avatar = models.URLField(blank=True, null=True, verbose_name="Аватар")
	email = models.EmailField(verbose_name='Почта')
