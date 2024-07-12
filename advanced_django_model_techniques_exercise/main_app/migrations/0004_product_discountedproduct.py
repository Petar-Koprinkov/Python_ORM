# Generated by Django 5.0.4 on 2024-07-12 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_book_movie_music'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('genre', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                'ordering': ['-created_at', 'title'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DiscountedProduct',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('main_app.product',),
        ),
    ]