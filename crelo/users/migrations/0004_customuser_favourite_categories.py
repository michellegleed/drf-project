# Generated by Django 3.0.8 on 2020-09-14 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_auto_20200914_0748'),
        ('users', '0003_customuser_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='favourite_categories',
            field=models.ManyToManyField(blank=True, related_name='customuser', to='projects.ProjectCategory'),
        ),
    ]