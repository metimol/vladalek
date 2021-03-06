# Generated by Django 4.0 on 2022-01-16 23:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('new_title', models.CharField(max_length=30, verbose_name='Название новости')),
                ('new_text', models.TextField(verbose_name='Текст новости')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата новости')),
            ],
            options={
                'verbose_name': 'Новость',
                'verbose_name_plural': 'Новости',
            },
        ),
    ]
