# Generated by Django 3.1.1 on 2020-10-26 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0023_auto_20201026_1346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='title',
            field=models.CharField(max_length=60),
        ),
    ]