from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.tests.factories import LocationFactory, TruckFactory


class TruckAPITestCase(APITestCase):
    """
    Тест-кейс для эндпоинтов грузовиков.
    """
    def setUp(self):
        self.truck = TruckFactory()
        self.location = LocationFactory()
        self.another_location = LocationFactory()
        self.list_url = reverse('truck-list')
        self.detail_url = reverse('truck-detail', args=[self.truck.id])

    def test_create_truck(self):
        """
        Тест возможности создания груза.
        """
        data = {
            'plate_number': '1234A',
            'location_zip': self.location.zip_code,
            'capacity': 200,
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_truck_without_location(self):
        """
        Тест возможности создания груза без локации.
        """
        data = {
            'plate_number': '1234A',
            'capacity': 200,
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_trucks(self):
        """
        Тест возможности получения списка грузовиков.
        """
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_truck(self):
        """
        Тест возможности изменения груза.
        """
        data = {
            'plate_number': '7777A',
            'location_zip': self.another_location.zip_code,
            'capacity': 1000,
        }
        response = self.client.put(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['plate_number'], data['plate_number'])
        self.assertEqual(response.data['location_zip'], data['location_zip'])

    def test_delete_truck(self):
        """
        Тест возможности удаления грузовика.
        """
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
