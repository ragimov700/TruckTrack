import django_filters
from geopy.distance import geodesic

from transport.models import Cargo, Truck


class CargoFilter(django_filters.FilterSet):
    """
    Фильтр для грузов, позволяющий фильтровать грузы по весу
    и расстоянию до грузовиков.
    """
    min_weight = django_filters.NumberFilter(field_name="weight",
                                             lookup_expr='gte')
    max_weight = django_filters.NumberFilter(field_name="weight",
                                             lookup_expr='lte')
    distance = django_filters.NumberFilter(method='filter_by_truck_distance')

    class Meta:
        model = Cargo
        fields = ['min_weight', 'max_weight', 'distance']

    def filter_by_truck_distance(self, queryset, name, value):
        filtered_ids = []
        trucks = list(Truck.objects.select_related('location'))
        for cargo in queryset:
            cargo_coords = (cargo.pickup_location.latitude,
                            cargo.pickup_location.longitude)
            for truck in trucks:
                if truck.location:
                    truck_coords = (truck.location.latitude,
                                    truck.location.longitude)
                    distance = geodesic(cargo_coords, truck_coords).miles
                    if distance <= value:
                        filtered_ids.append(cargo.id)
                        break
        return queryset.filter(id__in=filtered_ids)
