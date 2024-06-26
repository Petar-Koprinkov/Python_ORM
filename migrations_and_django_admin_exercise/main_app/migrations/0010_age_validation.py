from django.db import migrations


def age_validation(apps, schema_editor):
    person_model = apps.get_model("main_app", "Person")
    people = person_model.objects.all()

    for person in people:
        if person.age <= 12:
            person.age_group = "Child"
        elif person.age <= 17:
            person.age_group = "Teen"
        else:
            person.age_group = "Adult"

    person_model.objects.bulk_update(people, ["age_group"])


def reverse_age_validation(apps, schema_editor):
    person_model = apps.get_model("main_app", "Person")
    people = person_model.objects.all()

    for person in people:
        person.age_group = person_model._meta.get_field("age_group").default

    person_model.objects.bulk_update(people, ["age_group"])


class Migration(migrations.Migration):
    dependencies = [
        ('main_app', '0009_person'),
    ]

    operations = [
        migrations.RunPython(age_validation, reverse_age_validation)
    ]
