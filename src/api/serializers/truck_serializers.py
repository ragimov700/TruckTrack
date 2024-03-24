from decimal import Decimal

from geopy.distance import geodesic
from rest_framework import serializers

from transport.models import Truck, Location


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
            return round(distance, 2)
        return None


class TruckUpdateSerializer(serializers.ModelSerializer):
    location_zip = serializers.CharField(max_length=5)

    def update(self, instance, validated_data):
        new_location_zip = validated_data.get('location_zip')

        try:
            new_location = Location.objects.get(zip_code=new_location_zip)
            instance.location = new_location
        except Location.DoesNotExist:
            raise serializers.ValidationError({
                'location_zip': 'Локация с таким ZIP-кодом не существует.'
            })

        instance = super(TruckUpdateSerializer, self).update(instance,
                                                             validated_data)
        instance.save()
        serializer = TruckSerializer(instance)
        return serializer.data

    class Meta:
        model = Truck
        fields = ('id', 'plate_number', 'capacity', 'location_zip')