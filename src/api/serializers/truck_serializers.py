from geopy.distance import geodesic
from rest_framework import serializers

from transport.models import Truck


class TruckSerializer(serializers.ModelSerializer):
    location_zip = serializers.CharField(source='location.zip_code',
                                         read_only=True)

    class Meta:
        model = Truck
        fields = ('id', 'plate_number', 'capacity', 'location_zip')


class TruckDistanceSerializer(TruckSerializer):
    distance_to_cargo = serializers.SerializerMethodField()

    class Meta(TruckSerializer.Meta):
        fields = TruckSerializer.Meta.fields + ('distance_to_cargo',)

    def get_distance_to_cargo(self, obj):
        cargo = self.context.get('cargo')
        if cargo and obj.location:
            cargo_coords = (cargo.pickup_location.latitude,
                            cargo.pickup_location.longitude)
            truck_coords = (obj.location.latitude, obj.location.longitude)
            distance = geodesic(truck_coords, cargo_coords).miles
            return distance
        return None