from django.db import migrations


def price(apps, schema_editor):
    MULTIPLIER = 120
    smartphone_model = apps.get_model('main_app', 'smartphone')
    all_smartphones = smartphone_model.objects.all()

    for smartphone in all_smartphones:
        smartphone.price = len(smartphone.brand) * MULTIPLIER

    smartphone_model.objects.bulk_update(all_smartphones, ["price"])


def category(apps, schema_editor):
    smartphone_model = apps.get_model('main_app', 'smartphone')
    all_smartphones = smartphone_model.objects.all()

    for smartphone in all_smartphones:
        if smartphone.price >= 750:
            smartphone.category = 'Expensive'
        else:
            smartphone.category = 'Cheap'

    smartphone_model.objects.bulk_update( all_smartphones, ["category"])


def price_category(apps, schema_editor):
    price(apps, schema_editor)
    category(apps, schema_editor)


def reverse_price_category(apps, schema_editor):
    smartphone_model = apps.get_model('main_app', 'smartphone')
    all_smartphones = smartphone_model.objects.all()

    for smartphone in all_smartphones:
        smartphone.price = smartphone_model._meta.get_field("price").default
        smartphone.category = smartphone_model._meta.get_field("category").default

    smartphone_model.objects.bulk_update(all_smartphones, ["price", "category"])



class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0013_smartphone'),
    ]

    operations = [
        migrations.RunPython(price_category, reverse_price_category)
    ]
