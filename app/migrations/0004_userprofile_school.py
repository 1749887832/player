# Generated by Django 3.0.7 on 2020-10-21 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_schedule_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='school',
            field=models.CharField(max_length=64, null=True),
        ),
    ]