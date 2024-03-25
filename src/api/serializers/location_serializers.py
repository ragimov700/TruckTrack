from rest_framework import serializers

from transport.models import Location


class LocationSerializer(serializers.ModelSerializer):
    """
    Сериализатор локаций.
    """
    class Meta:
        model = Location
        fields = '__all__'
