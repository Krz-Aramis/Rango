# Generated by Django 2.0 on 2018-01-14 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0006_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='likes',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='category',
            name='views',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='picture',
            field=models.ImageField(blank=True, default='/default.jpg', upload_to='profile_images'),
        ),
    ]