from django.contrib import admin

from transport.models import Truck, Location, Cargo


@admin.register(Truck)
class TruckAdmin(admin.ModelAdmin):
    autocomplete_fields = ['location']


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    search_fields = ['city', 'state', 'zip']


@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    pass
