# Generated by Django 3.0.7 on 2020-10-23 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_player_basic'),
    ]

    operations = [
        migrations.AddField(
            model_name='player_basic',
            name='where_from',
            field=models.IntegerField(null=True),
        ),
    ]
