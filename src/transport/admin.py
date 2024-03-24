from django.contrib import admin

from transport.models import Cargo, Location, Truck


@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    """
    Конфигурация админ-панели для модели груза.
    """
    list_display = ('id', 'pickup_location', 'delivery_location', 'weight')
    autocomplete_fields = ['pickup_location', 'delivery_location']


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    """
    Конфигурация админ-панели для модели локации.
    """
    list_display = ('id', 'city', 'state', 'zip_code')
    search_fields = ('city', 'state', 'zip_code')


@admin.register(Truck)
class TruckAdmin(admin.ModelAdmin):
    """
    Конфигурация админ-панели для модели грузовика.
    """
    list_display = ('id', 'plate_number', 'capacity', 'location',)
    search_fields = ('plate_number',)
    autocomplete_fields = ('location',)
