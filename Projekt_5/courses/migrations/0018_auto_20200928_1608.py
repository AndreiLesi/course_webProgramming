# Generated by Django 3.1.1 on 2020-09-28 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0017_remove_course_newfield'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='image',
            field=models.URLField(blank=True, default='https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?fit=crop&w=500&q=60'),
        ),
    ]
