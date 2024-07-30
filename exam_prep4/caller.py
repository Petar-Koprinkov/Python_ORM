import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from django.db.models import Q, Count, Avg
from main_app.models import Author, Article, Review


def get_authors(search_name=None, search_email=None):
    if search_name is None and search_email is None:
        return ''

    search_name_query = Q(full_name__icontains=search_name)
    search_email_query = Q(email__icontains=search_email)

    if search_name is not None and search_email is not None:
        authors = Author.objects.filter(search_name_query & search_email_query).order_by('-full_name')
    elif search_email is None:
        authors = Author.objects.filter(search_name_query).order_by('-full_name')
    elif search_name is None:
        authors = Author.objects.filter(search_email_query).order_by('-full_name')

    if not authors:
        return ''

    result = []

    for author in authors:
        status = 'Banned' if author.is_banned is True else 'Not Banned'
        result.append(f'Author: {author.full_name}, email: {author.email}, status: {status}')

    return '\n'.join(result)


def get_top_publisher():
    author = Author.objects.get_authors_by_article_count().first()

    if author is None:
        return ''

    if not author.articles.all():
        return ''

    return f"Top Author: {author.full_name} with {author.article_count} published articles."


def get_top_reviewer():
    author = Author.objects.annotate(review_count=Count('author_reviews')).order_by('-review_count', 'email').first()

    if not author:
        return ''

    if not author.author_reviews.all():
        return ''

    return f"Top Reviewer: {author.full_name} with {author.review_count} published reviews."


def get_latest_article():
    article = Article.objects.prefetch_related(
        'authors', 'article_reviews'
    ).annotate(
        num_reviews=Count('article_reviews')
    ).order_by('-published_on').first()

    if article is None:
        return ''

    authors = []

    if not article.authors.all():
        return ''

    for author in article.authors.order_by('full_name'):
        authors.append(author.full_name)

    result = ', '.join(authors)

    avg_rating = article.article_reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    avg_rating_formatted = f"{avg_rating:.2f}"

    return (f"The latest article is: {article.title}. Authors: {result}. "
            f"Reviewed: {article.num_reviews} times. Average Rating: {avg_rating_formatted}.")


def get_top_rated_article():
    article = Article.objects.annotate(
        avg_reviews_rating=Avg('article_reviews__rating'),
        count_reviews=Count('article_reviews')
    ).filter(count_reviews__gt=0).order_by(
        '-avg_reviews_rating', 'title'
    ).first()

    if article is None:
        return ''

    if not article.article_reviews.all():
        return ''

    return (f"The top-rated article is: {article.title}, with an average rating of {article.avg_reviews_rating:.2f}, "
            f"reviewed {article.count_reviews} times.")


def ban_author(email=None):
    if email is None:
        return "No authors banned."

    author = Author.objects.filter(email=email).first()

    if author is None:
        return "No authors banned."

    num_reviews = author.author_reviews.count()

    for review in author.author_reviews.all():
        review.delete()

    author.is_banned = True
    author.save()

    return f"Author: {author.full_name} is banned! {num_reviews} reviews deleted."


