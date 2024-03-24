from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Truck, Location


@receiver(pre_save, sender=Truck)
def assign_default_location(sender, instance, **kwargs):
    if not instance.location:
        random_location = Location.objects.order_by('?').first()
        if random_location:
            instance.location = random_location
