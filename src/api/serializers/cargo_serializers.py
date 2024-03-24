from geopy.distance import geodesic
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.serializers.truck_serializers import TruckDistanceSerializer
from api.utils import get_surrounding_square
from transport.models import Cargo, Location, Truck


class CargoSerializer(serializers.ModelSerializer):
    """

    """
    pickup_location_zip = serializers.CharField(max_length=5)
    delivery_location_zip = serializers.CharField(max_length=5)

    def validate(self, data):
        pickup_location_zip = data.get(
            'pickup_location_zip',
            self.instance.pickup_location.zip_code if self.instance else None
        )
        delivery_location_zip = data.get(
            'delivery_location_zip',
            self.instance.delivery_location.zip_code if self.instance else None
        )

        if pickup_location_zip == delivery_location_zip:
            raise ValidationError(
                {'detail': 'Локации приема и доставки груза '
                           'не должны совпадать.'}
            )
        return data

    def create(self, validated_data):
        try:
            pickup_location_zip = validated_data.pop('pickup_location_zip')
            pickup_location = Location.objects.get(
                zip_code=pickup_location_zip
            )
        except Location.DoesNotExist:
            raise serializers.ValidationError(
                {'pickup_location_zip': 'Локация с таким ZIP-кодом '
                                        'для погрузки не существует.'})

        try:
            delivery_location_zip = validated_data.pop('delivery_location_zip')
            delivery_location = Location.objects.get(
                zip_code=delivery_location_zip
            )
        except Location.DoesNotExist:
            raise serializers.ValidationError(
                {'delivery_location_zip': 'Локация с таким ZIP-кодом '
                                          'для доставки не существует.'})

        cargo = Cargo.objects.create(
            pickup_location=pickup_location,
            delivery_location=delivery_location,
            **validated_data
        )
        detail_serializer = CargoDetailSerializer(cargo)
        return detail_serializer.data

    def update(self, instance, validated_data):
        new_pickup_location_zip = validated_data.get('pickup_location_zip')
        new_delivery_location_zip = validated_data.get('delivery_location_zip')
        if new_pickup_location_zip is not None:
            try:
                instance.pickup_location = Location.objects.get(
                    zip_code=new_pickup_location_zip
                )
            except Location.DoesNotExist:
                raise serializers.ValidationError(
                    {'pickup_location_zip': 'Локация с таким ZIP-кодом '
                                            'для погрузки не существует.'})
        if new_delivery_location_zip is not None:
            try:
                instance.delivery_location = Location.objects.get(
                    zip_code=new_delivery_location_zip
                )
            except Location.DoesNotExist:
                raise serializers.ValidationError(
                    {'delivery_location_zip': 'Локация с таким ZIP-кодом '
                                              'для доставки не существует.'})
        instance = super().update(instance, validated_data)
        instance.save()
        serializer = CargoDetailSerializer(instance)
        return serializer.data

    class Meta:
        model = Cargo
        fields = ('id', 'description', 'weight',
                  'pickup_location_zip', 'delivery_location_zip')


class CargoListSerializer(serializers.ModelSerializer):
    pickup_location_zip = serializers.CharField(
        source='pickup_location.zip_code',
        read_only=True
    )
    delivery_location_zip = serializers.CharField(
        source='delivery_location.zip_code',
        read_only=True
    )
    nearby_trucks_count = serializers.SerializerMethodField()

    def get_nearby_trucks_count(self, obj):
        square_coords = get_surrounding_square(
            obj.pickup_location.latitude,
            obj.pickup_location.longitude,
            450
        )
        trucks = Truck.objects.filter(
            location__latitude__gte=square_coords['min_lat'],
            location__latitude__lte=square_coords['max_lat'],
            location__longitude__gte=square_coords['min_lng'],
            location__longitude__lte=square_coords['max_lng'],
        )
        count = 0
        pickup_coords = (obj.pickup_location.latitude,
                         obj.pickup_location.longitude)
        for truck in trucks:
            truck_coords = (truck.location.latitude, truck.location.longitude)
            distance = geodesic(pickup_coords, truck_coords).miles
            if distance <= 450:
                count += 1
        return count

    class Meta:
        model = Cargo
        fields = ('id', 'description', 'weight',
                  'pickup_location_zip', 'delivery_location_zip',
                  'nearby_trucks_count')


class CargoDetailSerializer(serializers.ModelSerializer):
    pickup_location_zip = serializers.CharField(
        source='pickup_location.zip_code',
        read_only=True
    )
    delivery_location_zip = serializers.CharField(
        source='delivery_location.zip_code',
        read_only=True
    )
    trucks = serializers.SerializerMethodField()

    class Meta:
        model = Cargo
        fields = ('id', 'description', 'weight', 'pickup_location_zip',
                  'delivery_location_zip', 'trucks')

    def get_trucks(self, obj):
        trucks = Truck.objects.all()
        return TruckDistanceSerializer(trucks, many=True,
                                       context={'cargo': obj}).data
