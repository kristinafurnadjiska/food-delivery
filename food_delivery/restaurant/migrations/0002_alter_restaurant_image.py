# Generated by Django 4.2.4 on 2023-08-15 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='image',
            field=models.ImageField(default='default_restaurant.png', upload_to='restaurants/'),
        ),
    ]