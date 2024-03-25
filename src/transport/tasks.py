from celery import shared_task

from transport.models import Location, Truck


@shared_task
def update_truck_locations():
    """
    Задача для автоматического обновления местоположений грузовиков
    на случайное.
    """
    for truck in Truck.objects.all():
        new_location = Location.objects.order_by('?').first()
        if new_location:
            truck.location = new_location
            truck.save()
