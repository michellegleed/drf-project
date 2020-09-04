# Generated by Django 3.0.8 on 2020-09-01 23:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0027_auto_20200831_0838'),
        ('users', '0008_auto_20200901_2315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='favourite_categories',
            field=models.ManyToManyField(blank=True, default=None, null=True, related_name='customuser', to='projects.ProjectCategory'),
        ),
    ]
