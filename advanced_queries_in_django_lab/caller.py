import os

import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models
from main_app.models import Product, Category, Customer, Order, OrderProduct
from django.db.models import Sum, Avg, Count, Q, F
from decimal import Decimal


def product_quantity_ordered():
    result = []
    products = Product.objects.annotate(quantity=Sum('orderproduct__quantity')).exclude(quantity=None).order_by(
        '-quantity')

    for p in products:
        result.append(f'Quantity ordered of {p.name}: {p.quantity}')

    return '\n'.join(result)


def ordered_products_per_customer():
    result = []
    orders = Order.objects.prefetch_related('orderproduct_set__product__category').all()

    for order in orders:
        result.append(f'Order ID: {order.id}, Customer: {order.customer.username}')
        for product in order.products.all():
            result.append(f'- Product: {product.name}, Category: {product.category.name}')

    return '\n'.join(result)


def filter_products():
    result = []
    products = Product.objects.filter(Q(is_available=True) & Q(price__gt=3.00)).order_by('-price', 'name')

    for product in products:
        result.append(f'{product.name}: {product.price}lv.')

    return '\n'.join(result)


def give_discount():
    Product.objects.filter(Q(is_available=True) & Q(price__gt=3.00)).update(price=F('price') * 0.7)

    all_available_products = (Product.objects.filter(is_available=True).order_by('-price', 'name'))

    result = []
    for product in all_available_products:
        result.append(f"{product.name}: {product.price}lv.")
    return "\n".join(result)



