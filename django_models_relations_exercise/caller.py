import os
from datetime import timedelta, date

import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Author, Book, Song, Artist, Product, Review, Driver, DrivingLicense, Owner, Car, Registration


def show_all_authors_with_their_books():
    authors = Author.objects.all()
    result = []

    for author in authors:
        books = author.book_set.all()
        if not books:
            continue

        books_list = ', '.join(book.title for book in books)

        result.append(f"{author.name} has written - {books_list}!")

    return '\n'.join(result)


def delete_all_authors_without_books():
    Author.objects.filter(book__isnull=True).delete()


def add_song_to_artist(artist_name: str, song_title: str):
    artist = Artist.objects.get(name=artist_name)
    song = Song.objects.get(title=song_title)
    artist.songs.add(song)


def get_songs_by_artist(artist_name: str):
    return Artist.objects.get(name=artist_name).songs.all().order_by('-id')
    #return Song.objects.filter(artists__name=artist_name).order_by('-id')


def remove_song_from_artist(artist_name: str, song_title: str):
    artist = Artist.objects.get(name=artist_name)
    song = Song.objects.get(title=song_title)
    artist.songs.remove(song)


def calculate_average_rating_for_product_by_name(product_name: str):
    product = Product.objects.get(name=product_name)
    reviews = product.reviews.all()
    rating = 0
    for review in reviews:
        rating += review.rating

    return rating / len(reviews)


def get_reviews_with_high_ratings(threshold: int):
    return Review.objects.filter(rating__gte=threshold)


def get_products_with_no_reviews():
    return Product.objects.filter(reviews__isnull=True).order_by('-name')


def delete_products_without_reviews():
    Product.objects.filter(reviews__isnull=True).delete()


def calculate_licenses_expiration_dates():
    licenses = DrivingLicense.objects.all().order_by('-license_number')
    result = []
    for license in licenses:
        result.append(f'License with number: {license.license_number} expires on {license.issue_date + timedelta(days=365)}!')
    return '\n'.join(result)


def get_drivers_with_expired_licenses(due_date: date):
    return Driver.objects.filter(license__issue_date__gt=due_date - timedelta(days=365))


def register_car_by_owner(owner: Owner):
    registration = Registration.objects.filter(car__isnull=True).first()
    car = Car.objects.filter(registration__isnull=True).first()

    owner.cars.add(car)


    registration.registration_date = date.today()

    registration.car = car
    registration.save()

    return (f'Successfully registered {car.model} to {owner.name} with '
            f'registration number {registration.registration_number}.')


# Create owners
owner1 = Owner.objects.create(name='Ivelin Milchev')
owner2 = Owner.objects.create(name='Alice Smith')

# Create cars
car1 = Car.objects.create(model='Citroen C5', year=2004)
car2 = Car.objects.create(model='Honda Civic', year=2021)
# Create instances of the Registration model for the cars
registration1 = Registration.objects.create(registration_number='TX0044XA')
registration2 = Registration.objects.create(registration_number='XYZ789')

print(register_car_by_owner(owner1))
