# Generated by Django 3.0.8 on 2020-08-30 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0015_auto_20200830_0456'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='is_open',
            field=models.BooleanField(blank=True, default=True),
        ),
    ]
