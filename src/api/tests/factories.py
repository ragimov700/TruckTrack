import factory
from faker import Faker

from transport.models import Cargo, Location

fake = Faker()


class LocationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Location

    zip_code = factory.Sequence(lambda n: '%05d' % n)
    latitude = factory.LazyFunction(lambda: fake.latitude())
    longitude = factory.LazyFunction(lambda: fake.longitude())


class CargoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Cargo

    description = factory.Faker('text')
    weight = factory.Faker('random_int', min=1, max=1000)
    pickup_location = factory.SubFactory(LocationFactory)
    delivery_location = factory.SubFactory(LocationFactory)
