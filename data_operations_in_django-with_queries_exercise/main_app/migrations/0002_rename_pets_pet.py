# Generated by Django 5.0.4 on 2024-06-28 09:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Pets',
            new_name='Pet',
        ),
    ]
