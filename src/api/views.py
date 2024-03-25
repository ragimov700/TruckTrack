from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets

from api.filters import CargoFilter
from api.schemas import cargo_schema, locations_schema, trucks_schema
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


@extend_schema(tags=['Грузы'])
@extend_schema_view(**cargo_schema)
class CargoViewSet(viewsets.ModelViewSet):
    """
    ViewSet для обработки запросов к грузам.
    """
    queryset = Cargo.objects.select_related(
        'pickup_location',
        'delivery_location'
    ).order_by('id')
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CargoFilter

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


@extend_schema(tags=['Локации'])
@extend_schema_view(**locations_schema)
class LocationViewSet(viewsets.ModelViewSet):
    """
    ViewSet для обработки запросов к локациям.
    """
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


@extend_schema(tags=['Грузовики'])
@extend_schema_view(**trucks_schema)
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
