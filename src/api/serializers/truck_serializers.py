from geopy.distance import geodesic
from rest_framework import serializers

from transport.models import Location, Truck


class TruckReadSerializer(serializers.ModelSerializer):
    location_zip = serializers.CharField(source='location.zip_code',
                                         read_only=True)

    class Meta:
        model = Truck
        fields = ('id', 'plate_number', 'capacity', 'location_zip')


class TruckDistanceSerializer(TruckReadSerializer):
    distance_to_cargo = serializers.SerializerMethodField()

    class Meta(TruckReadSerializer.Meta):
        fields = TruckReadSerializer.Meta.fields + ('distance_to_cargo',)

    def get_distance_to_cargo(self, obj):
        cargo = self.context.get('cargo')
        if cargo and obj.location:
            cargo_coords = (cargo.pickup_location.latitude,
                            cargo.pickup_location.longitude)
            truck_coords = (obj.location.latitude, obj.location.longitude)
            distance = geodesic(truck_coords, cargo_coords).miles
            return round(distance, 2)
        return None


class TruckSerializer(serializers.ModelSerializer):
    location_zip = serializers.CharField(max_length=5, required=False)

    def create(self, validated_data):
        location_zip = validated_data.pop('location_zip', None)
        location = None
        if location_zip is not None:
            try:
                location = Location.objects.get(zip_code=location_zip)
            except Location.DoesNotExist:
                raise serializers.ValidationError(
                    {'location_zip': 'Локация с таким ZIP-кодом '
                                     'для погрузки не существует.'}
                )
        truck = Truck.objects.create(location=location, **validated_data)
        serializer = TruckReadSerializer(truck)
        return serializer.data

    def update(self, instance, validated_data):
        new_location_zip = validated_data.get('location_zip')

        try:
            new_location = Location.objects.get(zip_code=new_location_zip)
            instance.location = new_location
        except Location.DoesNotExist:
            raise serializers.ValidationError({
                'location_zip': 'Локация с таким ZIP-кодом не существует.'
            })

        instance = super().update(instance, validated_data)
        instance.save()
        serializer = TruckReadSerializer(instance)
        return serializer.data

    class Meta:
        model = Truck
        fields = ('id', 'plate_number', 'capacity', 'location_zip')
