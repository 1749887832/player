# Generated by Django 3.1.3 on 2020-12-03 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_tactics'),
    ]

    operations = [
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=68, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='schedule',
            name='season_id',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]