import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Director, Actor, Movie
from django.db.models import Count, Avg, Q, F


def get_directors(search_name=None, search_nationality=None):
    if search_name is None and search_nationality is None:
        return ''

    if search_name is not None and search_nationality is not None:
        directors = Director.objects.filter(full_name__icontains=search_name,
                                            nationality__icontains=search_nationality).order_by('full_name')
    elif search_name is None:
        directors = Director.objects.filter(nationality__icontains=search_nationality).order_by('full_name')
    elif search_nationality is None:
        directors = Director.objects.filter(full_name__icontains=search_name).order_by('full_name')

    if not directors:
        return ''

    result = []
    for d in directors:
        result.append(f'Director: {d.full_name}, nationality: {d.nationality}, experience: {d.years_of_experience}')
    return '\n'.join(result)


def get_top_director():
    director = Director.objects.get_directors_by_movies_count().first()

    if director is None:
        return ''

    return f"Top Director: {director.full_name}, movies: {director.movie_count}."


def get_top_actor():
    actor = Actor.objects.annotate(movie_count=Count('starring_actor_movies'),
                                   avg_rating=Avg('starring_actor_movies__rating')
                                   ).order_by('-movie_count', 'full_name').first()

    if actor is None or not actor.movie_count:
        return ''

    movies = ', '.join(actor.starring_actor_movies.values_list('title', flat=True))

    return f"Top Actor: {actor.full_name}, starring in movies: {movies}, movies average rating: {actor.avg_rating:.1f}"


def get_actors_by_movies_count():
    actors = Actor.objects.annotate(movie_count=Count('actor_movies')).order_by('-movie_count', 'full_name')[:3]

    if not actors:
        return ''
    for a in actors:
        if not a.movie_count:
            return ''

    result = []

    for a in actors:
        result.append(f'{a.full_name}, participated in {a.movie_count} movies')

    return '\n'.join(result)


def get_top_rated_awarded_movie():
    movie = Movie.objects.select_related('starring_actor').prefetch_related('actors').filter(is_awarded=True).order_by(
        '-rating', 'title').first()

    if movie is None:
        return ''

    starring_actor = movie.starring_actor.full_name if movie.starring_actor else 'N/A'
    cast = ', '.join(movie.actors.order_by('full_name').values_list('full_name', flat=True))
    return (f"Top rated awarded movie: {movie.title}, rating: {movie.rating:.1f}. Starring actor: {starring_actor}. "
            f"Cast: {cast}.")


def increase_rating():
    movies = Movie.objects.filter(is_classic=True, rating__lt=10.0)

    if not movies:
        return "No ratings increased."

    count = movies.count()
    movies.update(rating=F('rating') + 0.1)

    return f"Rating increased for {count} movies."
