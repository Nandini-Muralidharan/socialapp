# Generated by Django 4.1.2 on 2022-12-27 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialnetworkapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images'),
        ),
    ]
