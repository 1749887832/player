# Generated by Django 3.0.7 on 2020-11-09 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_signup'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player_basic',
            name='specialty',
        ),
        migrations.AddField(
            model_name='player_data',
            name='specialty',
            field=models.CharField(max_length=64, null=True),
        ),
    ]
