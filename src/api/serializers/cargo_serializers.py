from geopy.distance import geodesic
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.serializers.truck_serializers import TruckDistanceSerializer
from transport.models import Cargo, Location


class CargoSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания, обновления и валидации грузов.

    Валидирует, что локации погрузки и разгрузки груза не совпадают.
    При создании или обновлении груза, использует почтовый индекс для
    нахождения соответствующих локаций погрузки и разгрузки.
    """
    pickup_location_zip = serializers.CharField(max_length=5,
                                                write_only=True)
    delivery_location_zip = serializers.CharField(max_length=5,
                                                  write_only=True)

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
                                        'для погрузки не существует.'}
            )

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
        return cargo

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
    """
    Сериализатор для представления списка грузов.

    Включает в себя количество ближайших грузовиков в пределах 450 миль от
    места погрузки каждого груза.
    """
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
        trucks = self.context.get('trucks', [])
        pickup_coords = (obj.pickup_location.latitude,
                         obj.pickup_location.longitude)

        count = 0
        for truck in trucks:
            truck_coords = (truck.location.latitude, truck.location.longitude)
            distance = geodesic(truck_coords, pickup_coords).miles
            if distance <= 450:
                count += 1

        return count

    class Meta:
        model = Cargo
        fields = ('id', 'description', 'weight',
                  'pickup_location_zip', 'delivery_location_zip',
                  'nearby_trucks_count')


class CargoDetailSerializer(serializers.ModelSerializer):
    """
    Сериализатор для представления детальной информации о грузе.

    Помимо основной информации о грузе, включает в себя список всех грузовиков
    с расстоянием до груза.
    """
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
        trucks = self.context.get('trucks', [])
        return TruckDistanceSerializer(trucks, many=True,
                                       context={'cargo': obj}).data
