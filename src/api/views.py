from rest_framework import viewsets

from api.serializers import (
    CargoSerializer,
    LocationSerializer,
    TruckSerializer,
)
from transport.models import Cargo, Location, Truck


class CargoViewSet(viewsets.ModelViewSet):
    queryset = Cargo.objects.all()
    serializer_class = CargoSerializer


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class TruckViewSet(viewsets.ModelViewSet):
    queryset = Truck.objects.all()
    serializer_class = TruckSerializer
