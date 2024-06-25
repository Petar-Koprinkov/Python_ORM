from django.db import migrations
import random


def create_random_barcode(apps, schema_editor):
    Product = apps.get_model('main_app', 'Product')
    all_products = Product.objects.all()
    all_barcodes = random.sample(range(100_000_000, 1_000_000_000), len(all_products))

    for product, barcode_code in zip(all_products, all_barcodes):
        product.barcode = barcode_code
        product.save()


def reverse_random_barcode(apps, schema_editor):
    Product = apps.get_model('main_app', 'Product')
    for product in Product.objects.all():
        product.barcode = 0
        product.save()


class Migration(migrations.Migration):
    dependencies = [
        ('main_app', '0004_product_barcode'),
    ]

    operations = [
        migrations.RunPython(create_random_barcode, reverse_random_barcode)
    ]
