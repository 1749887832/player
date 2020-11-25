# Generated by Django 3.0.7 on 2020-10-22 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_userprofile_school'),
    ]

    operations = [
        migrations.CreateModel(
            name='Player_Basic',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('p_id', models.CharField(default='集训球员', max_length=32)),
                ('state', models.CharField(default='健康', max_length=32)),
                ('number', models.IntegerField(null=True)),
                ('position', models.CharField(max_length=32, null=True)),
                ('specialty', models.CharField(max_length=64, null=True)),
                ('enable', models.IntegerField(default=1)),
                ('user_id', models.IntegerField()),
            ],
        ),
    ]