import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Astronaut, Spacecraft, Mission
from django.db.models import Q, Count, Sum, F, Avg


def get_astronauts(search_string=None):
    if search_string is None:
        return ''

    astronauts = Astronaut.objects.filter(
        Q(name__icontains=search_string)
        |
        Q(phone_number__icontains=search_string)
    ).order_by('name')

    if not astronauts.exists():
        return ''

    result = []

    for a in astronauts:
        status = 'Active' if a.is_active is True else 'Inactive'
        result.append(f'Astronaut: {a.name}, phone number: {a.phone_number}, status: {status}')

    return '\n'.join(result)


def get_top_astronaut():
    astronaut = Astronaut.objects.get_astronauts_by_missions_count().first()

    if not astronaut:
        return "No data."

    if not astronaut.missions_count:
        return "No data."

    return f"Top Astronaut: {astronaut.name} with {astronaut.missions_count} missions."


def get_top_commander():
    commander = Astronaut.objects.annotate(
        commanded_mission=Count('commander_missions')
    ).order_by(
        '-commanded_mission',
        'phone_number'
    ).first()

    if commander is None:
        return "No data."

    if not commander.commanded_mission:
        return "No data."

    return f"Top Commander: {commander.name} with {commander.commanded_mission} commanded missions."


def get_last_completed_mission():
    mission = Mission.objects.filter(
        status='Completed'
    ).annotate(
        total_spacewalks=Sum('astronauts__spacewalks')
    ).order_by(
        '-launch_date'
    ).first()

    if mission is None:
        return "No data."

    commander = mission.commander.name if mission.commander else "TBA"

    astronauts = ', '.join(mission.astronauts.order_by('name').values_list('name', flat=True))

    return (f"The last completed mission is: {mission.name}. Commander: {commander}. "
            f"Astronauts: {astronauts}. Spacecraft: {mission.spacecraft.name}. Total spacewalks: {mission.total_spacewalks}.")


def get_most_used_spacecraft():
    spacecraft = Spacecraft.objects.annotate(
        missions_count=Count('spacecraft_missions')
    ).order_by(
        '-missions_count',
        'name'
    ).first()

    if spacecraft is None:
        return "No data."

    if not spacecraft.missions_count:
        return "No data."

    num_astronauts = Mission.objects.filter(
        spacecraft=spacecraft
    ).values_list(
        'astronauts', flat=True
    ).distinct().count()

    return (f"The most used spacecraft is: {spacecraft.name}, manufactured by {spacecraft.manufacturer}, "
            f"used in {spacecraft.missions_count} missions, astronauts on missions: {num_astronauts}.")


def decrease_spacecrafts_weight():

    planned_missions = Mission.objects.filter(status=Mission.StatusChoices.PLANNED)

    spacecraft = planned_missions.values_list(
        'spacecraft_id', flat=True
    ).distinct()

    spacecrafts_update = Spacecraft.objects.filter(
        id__in=spacecraft, weight__gte=200.0
    )

    if not spacecrafts_update:
        return "No changes in weight."

    num_of_spacecrafts = spacecrafts_update.update(
        weight=F('weight') - 200.0
    )

    avg_weight = Spacecraft.objects.all().aggregate(
        avg_weight=Avg('weight')
    )['avg_weight']

    return (f"The weight of {num_of_spacecrafts} spacecrafts has been decreased. "
            f"The new average weight of all spacecrafts is {avg_weight}kg")