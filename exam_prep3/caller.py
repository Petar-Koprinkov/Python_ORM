import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from django.db.models import Q, Count
from main_app.models import TennisPlayer, Tournament, Match


def get_tennis_players(search_name=None, search_country=None):
    if search_name is None and search_country is None:
        return ''

    name_query = Q(full_name__icontains=search_name)
    country_query = Q(country__icontains=search_country)

    if search_name is not None and search_country is not None:
        players = TennisPlayer.objects.filter(name_query & country_query).order_by('ranking')
    elif search_name is None:
        players = TennisPlayer.objects.filter(country_query).order_by('ranking')
    elif search_country is None:
        players = TennisPlayer.objects.filter(name_query).order_by('ranking')

    if not players:
        return ''

    result = []

    for p in players:
        result.append(f'Tennis Player: {p.full_name}, country: {p.country}, ranking: {p.ranking}')

    return '\n'.join(result)


def get_top_tennis_player():
    player = TennisPlayer.objects.get_tennis_players_by_wins_count().first()

    if player is None:
        return ''

    return f'Top Tennis Player: {player.full_name} with {player.win_count} wins.'


def get_tennis_player_by_matches_count():
    player = TennisPlayer.objects.annotate(match_count=Count('player_matches')).order_by('-match_count',
                                                                                         'ranking').first()

    if player is None:
        return ''

    if not player.match_count:
        return ''

    return f'Tennis Player: {player.full_name} with {player.match_count} matches played.'


def get_tournaments_by_surface_type(surface=None):
    if surface is None:
        return ''

    tournaments = Tournament.objects.filter(surface_type__icontains=surface).order_by('-start_date')

    if not tournaments:
        return ''

    result = []

    for t in tournaments:
        result.append(f'Tournament: {t.name}, start date: {t.start_date}, matches: {t.tournament_matches.count()}')

    return '\n'.join(result)


def get_latest_match_info():
    match = Match.objects.order_by('-date_played', '-id').first()

    if match is None:
        return ''

    winner = match.winner.full_name if match.winner else 'TBA'
    players = " vs ".join(match.players.order_by('full_name').values_list('full_name', flat=True))

    return (f"Latest match played on: {match.date_played}, tournament: {match.tournament.name}, score: {match.score}, "
            f"players: {players}, winner: {winner}, summary: {match.summary}")


def get_matches_by_tournament(tournament_name=None):
    if tournament_name is None:
        return "No matches found."

    tournament = Tournament.objects.prefetch_related('tournament_matches__players').filter(name=tournament_name).first()

    if tournament is None:
        return "No matches found."

    if not tournament.tournament_matches.all():
        return "No matches found."

    result = []

    for m in tournament.tournament_matches.order_by('-date_played'):
        winner = m.winner.full_name if m.winner else 'TBA'
        result.append(f'Match played on: {m.date_played}, score: {m.score}, winner: {winner}')

    return '\n'.join(result)




















