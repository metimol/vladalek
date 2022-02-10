# Generated by Django 4.0 on 2022-02-04 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_alter_articles_pub_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='TemporaryCategories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(help_text='Название категории', max_length=25, verbose_name='Категория')),
                ('category_code', models.TextField(verbose_name='Код')),
            ],
        ),
    ]