from django.db import migrations
from django.utils import timezone


def update_delivery_and_warranty(apps, schema_editor):
    order_model = apps.get_model('main_app', 'Order')
    all_orders = order_model.objects.all()

    for order in all_orders:
        if order.status == "Pending":
            order.delivery = order.order_date + timezone.timedelta(days=3)
        elif order.status == "Completed":
            order.warranty = "24 months"
        elif order.status == "Canceled":
            order.delete()

    order_model.objects.bulk_update(all_orders, ['delivery', 'warranty'])


def reverse_delivery_and_warranty(apps, schema_editor):
    order_model = apps.get_model('main_app', 'Order')
    all_orders = order_model.objects.all()

    for order in all_orders:
        if order.status == "Pending":
            order.delivery = None
        elif order.status == "Completed":
            order.warranty = order_model._meta.get_field('warranty').default

    order_model.objects.bulk_update(all_orders, ['delivery', 'warranty'])


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0015_order'),
    ]

    operations = [
        migrations.RunPython(update_delivery_and_warranty, reverse_delivery_and_warranty)
    ]