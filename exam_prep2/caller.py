import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Profile, Product, Order
from django.db.models import Q, Count, F
from populate_data import populate_model_with_data


def get_profiles(search_string=None):
    if search_string is None:
        return ''

    full_name_query = Q(full_name__icontains=search_string)
    email_query = Q(email__icontains=search_string)
    phone_number_query = Q(phone_number__icontains=search_string)

    if Profile.objects.filter(full_name_query):
        profiles = Profile.objects.filter(full_name_query).order_by('full_name')
    elif Profile.objects.filter(email_query):
        profiles = Profile.objects.filter(email_query).order_by('full_name')
    elif Profile.objects.filter(phone_number_query):
        profiles = Profile.objects.filter(phone_number_query).order_by('full_name')
    else:
        return ''

    result = []

    for p in profiles:
        result.append(
            f'Profile: {p.full_name}, email: {p.email}, phone number: {p.phone_number}, orders: {p.profile_orders.count()}')

    return '\n'.join(result)


def get_loyal_profiles():
    profiles = Profile.objects.get_regular_customers()

    if not profiles:
        return ''

    result = []
    for p in profiles:
        result.append(f'Profile: {p.full_name}, orders: {p.orders_count}')

    return '\n'.join(result)


def get_last_sold_products():
    order = Order.objects.order_by('-creation_date').first()  # prefetch_related
   
    if order is None or not products:  
        return ''
        
     products = ', '.join(order.products.all().order_by('name').values_list('name', flat=True))

    return f"Last sold products: {products}"


def get_top_products():
    products = Product.objects.annotate(order_count=Count('product_orders')).filter(order_count__gt=0).order_by(
        '-order_count', 'name')[:5]

    if not products:
        return ''

    for p in products:
        if not p.order_count:
            return ''

    result = [f'Top products:']

    for p in products:
        result.append(f'{p.name}, sold {p.order_count} times')

    return '\n'.join(result)


def apply_discounts():
    order = Order.objects.annotate(products_count=Count('products')).filter(products_count__gt=2, is_completed=False)

    if not order:
        num_of_updated_orders = 0
    else:
        num_of_updated_orders = order.count()

        order.update(
            total_price=F('total_price') * 0.90
        )

    return f"Discount applied to {num_of_updated_orders} orders."


def complete_order():
    order = Order.objects.filter(is_completed=False).order_by('creation_date').first()

    if not order:
        return ''

    for product in order.products.all():
        product.in_stock -= 1
        if product.in_stock == 0:
            product.is_available = False
        product.save()

    order.is_completed = True
    order.save()

    return "Order has been completed!"

