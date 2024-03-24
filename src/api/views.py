from rest_framework import viewsets

from api.serializers.cargo_serializers import (
    CargoCreateSerializer,
    CargoDetailSerializer,
    CargoListSerializer,
)
from api.serializers.location_serializers import LocationSerializer
from api.serializers.truck_serializers import TruckSerializer, \
    TruckUpdateSerializer
from transport.models import Cargo, Location, Truck


class CargoViewSet(viewsets.ModelViewSet):
    queryset = Cargo.objects.all()

    def get_serializer_class(self):
        match self.action:
            case 'list':
                return CargoListSerializer
            case 'retrieve':
                return CargoDetailSerializer
            case _:
                return CargoCreateSerializer


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class TruckViewSet(viewsets.ModelViewSet):
    queryset = Truck.objects.all()

    def get_serializer_class(self):
        match self.action:
            case 'partial_update' | 'update':
                return TruckUpdateSerializer