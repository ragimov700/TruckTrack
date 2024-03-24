from rest_framework import serializers

from transport.models import Cargo, Location, Truck


class CargoSerializer(serializers.ModelSerializer):
    pickup_location_zip = serializers.CharField(
        source='pickup_location.zip_code',
        read_only=True
    )
    delivery_location_zip = serializers.CharField(
        source='delivery_location.zip_code',
        read_only=True
    )

    class Meta:
        model = Cargo
        fields = ('id', 'description', 'weight',
                  'pickup_location_zip', 'delivery_location_zip')


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class TruckSerializer(serializers.ModelSerializer):
    location_zip = serializers.CharField(source='location.zip_code',
                                         read_only=True)

    class Meta:
        model = Truck
        fields = ('id', 'plate_number', 'capacity', 'location_zip')
