import os
import django
from django.db.models import QuerySet

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Author, Book, Review


def find_books_by_genre_and_language(genre: str, language: str) -> QuerySet:
    books = Book.objects.filter(genre=genre, language=language)
    return books


def find_authors_nationalities():
    authors = Author.objects.filter(nationality__isnull=False)
    return "\n".join([f"{author.first_name} {author.last_name} is {author.nationality}" for author in authors])


def order_books_by_year():
    books = Book.objects.all().order_by('publication_year', 'title')
    return "\n".join([f"{book.publication_year} year: {book.title} by {book.author}" for book in books])


def delete_review_by_id(reviewer_id):
    review = Review.objects.get(id=reviewer_id)
    review.delete()
    return f"Review by {review.reviewer_name} was deleted"


def filter_authors_by_nationalities(nationality: str) -> str:
    authors = Author.objects.filter(nationality=nationality).order_by('first_name', 'last_name')
    result = []
    for author in authors:
        if author.biography is not None:
            result.append(author.biography)
        else:
            result.append(f"{author.first_name} {author.last_name}")

    return '\n'.join(result)


def filter_authors_by_birth_year(first_year, last_year):
    authors = Author.objects.filter(birth_date__year__range=(first_year, last_year)).order_by('-birth_date')
    return '\n'.join(f"{author.birth_date}: {author.first_name} {author.last_name}" for author in authors)


def change_reviewer_name(old_name, new_name):
    Review.objects.filter(reviewer_name=old_name).update(reviewer_name=new_name)
    return Review.objects.all()


