from django.db import migrations


def unique_brands_names(apps, schema_editor):
    shoe_model = apps.get_model('main_app', 'Shoe')
    unique_brands_names = shoe_model.objects.values_list('brand', flat=True).distinct()
    unique_brands_model = apps.get_model('main_app', 'UniqueBrands')

    unique_brands_model.objects.bulk_create(
        [unique_brands_model(brand_name=unique_brands_name) for unique_brands_name in unique_brands_names]
    )


def reverse_unique_brands_names(apps, schema_editor):
    unique_brands_model = apps.get_model('main_app', 'UniqueBrands')
    unique_brands_model.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('main_app', '0002_uniquebrands'),
    ]

    operations = [
        migrations.RunPython(unique_brands_names, reverse_unique_brands_names)
    ]
