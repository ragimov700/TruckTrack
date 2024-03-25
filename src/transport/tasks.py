from celery import shared_task
from transport.models import Truck, Location


@shared_task
def update_truck_locations():
    for truck in Truck.objects.all():
        new_location = Location.objects.order_by('?').first()
        truck.location = new_location
        truck.save()
