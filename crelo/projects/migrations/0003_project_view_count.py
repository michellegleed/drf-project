# Generated by Django 3.0.8 on 2020-09-14 00:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_auto_20200904_2332'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='view_count',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
