# Generated by Django 4.1.7 on 2023-03-08 23:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_alter_articles_options_alter_categories_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articles',
            name='fixed',
        ),
    ]
