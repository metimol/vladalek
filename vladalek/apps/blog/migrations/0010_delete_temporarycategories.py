# Generated by Django 4.1 on 2022-12-18 12:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_alter_articles_favorites'),
    ]

    operations = [
        migrations.DeleteModel(
            name='TemporaryCategories',
        ),
    ]
