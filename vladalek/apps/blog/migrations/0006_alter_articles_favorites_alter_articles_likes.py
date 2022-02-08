# Generated by Django 4.0 on 2022-02-07 23:43

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0005_alter_temporarycategories_options_articles_favorites_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articles',
            name='favorites',
            field=models.ManyToManyField(blank=True, null=True, related_name='favourites', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='articles',
            name='likes',
            field=models.ManyToManyField(blank=True, null=True, related_name='likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
