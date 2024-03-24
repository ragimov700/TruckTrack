import random
import string

import factory
from faker import Faker

from transport.models import Cargo, Location, Truck

fake = Faker()


class LocationFactory(factory.django.DjangoModelFactory):
    """
    Фабрика для модели локации.
    """
    class Meta:
        model = Location

    zip_code = factory.Sequence(lambda n: '%05d' % n)
    latitude = factory.LazyFunction(lambda: fake.latitude())
    longitude = factory.LazyFunction(lambda: fake.longitude())


class CargoFactory(factory.django.DjangoModelFactory):
    """
    Фабрика для модели груза.
    """
    class Meta:
        model = Cargo

    description = factory.Faker('text')
    weight = factory.Faker('random_int', min=1, max=1000)
    pickup_location = factory.SubFactory(LocationFactory)
    delivery_location = factory.SubFactory(LocationFactory)


class TruckFactory(factory.django.DjangoModelFactory):
    """
    Фабрика для модели грузовиков.
    """
    class Meta:
        model = Truck

    # Генерация случайного номерного знака
    plate_number = factory.LazyAttribute(
        lambda x: f"{random.randint(1000, 9999)}"
                  f"{random.choice(string.ascii_uppercase)}"
    )
    capacity = factory.Faker('random_int', min=100, max=1000)
    location = factory.SubFactory(LocationFactory)
