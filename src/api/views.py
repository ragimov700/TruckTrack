from rest_framework import viewsets

from api.serializers.cargo_serializers import (
    CargoDetailSerializer,
    CargoListSerializer,
    CargoSerializer,
)
from api.serializers.location_serializers import LocationSerializer
from api.serializers.truck_serializers import (
    TruckReadSerializer,
    TruckSerializer,
)
from transport.models import Cargo, Location, Truck


class CargoViewSet(viewsets.ModelViewSet):
    """
    ViewSet для обработки запросов к грузам.
    """
    queryset = Cargo.objects.select_related(
        'pickup_location',
        'delivery_location'
    ).order_by('id')

    def get_serializer_class(self):
        match self.action:
            case 'list':
                return CargoListSerializer
            case 'retrieve':
                return CargoDetailSerializer
            case _:
                return CargoSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        match self.action:
            case 'list' | 'retrieve':
                context['trucks'] = Truck.objects.select_related('location')
                return context
            case _:
                return context


class LocationViewSet(viewsets.ModelViewSet):
    """
    ViewSet для обработки запросов к локациям.
    """
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class TruckViewSet(viewsets.ModelViewSet):
    """
    ViewSet для обработки запросов к грузовикам.
    """
    queryset = Truck.objects.select_related('location').order_by('id')

    def get_serializer_class(self):
        match self.action:
            case 'list' | 'retrieve':
                return TruckReadSerializer
            case _:
                return TruckSerializer
