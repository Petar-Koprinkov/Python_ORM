# Generated by Django 5.0.4 on 2024-06-23 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0008_book_alter_exercise_video_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=8),
        ),
    ]
