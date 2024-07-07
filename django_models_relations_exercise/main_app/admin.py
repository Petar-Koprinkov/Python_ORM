from django.contrib import admin

from main_app.models import Car, Owner, Registration


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('model', 'year', 'owner', 'car_details')

    @staticmethod
    def car_details(car: Car):
        try:
            owner = car.owner.name
        except AttributeError:
            owner = "No owner"

        try:
            registration = car.registration.registration_number
        except AttributeError:
            registration = "No registration number"

        return f"Owner: {owner}, Registration: {registration}"

    car_details.short_description = 'Cars Details'


@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner_car')

    @staticmethod
    def owner_car(owner: Owner):

        try:
            car = owner.cars.first().model
        except AttributeError:
            car = "No car"

        return car

    owner_car.short_description = 'Car'


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('registration_number', 'registration_date', 'car_model')

    @staticmethod
    def car_model(registration: Registration):
        try:
            car = registration.car.model
        except AttributeError:
            car = "No car"

        return car


    car_model.short_description = 'Car'

