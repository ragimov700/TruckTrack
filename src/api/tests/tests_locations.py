from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.tests.factories import LocationFactory


class LocationAPITestCase(APITestCase):
    """
    Тест-кейс для модели локации.
    """
    def setUp(self):
        self.location = LocationFactory()
        self.list_url = reverse('location-list')
        self.detail_url = reverse('location-detail', args=[self.location.id])

    def test_create_location(self):
        """
        Тест возможности создания локации.
        """
        data = {
            'city': 'Москва',
            'zip_code': '12345',
            'state': 'МО',
            'latitude': '11.11111',
            'longitude': '22.22222'
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_locations(self):
        """
        Тест возможности получения списка локаций.
        """
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_location(self):
        """
        Тест возможности изменения локации.
        """
        data = {
            'city': 'Новый город',
            'zip_code': '22222',
            'state': 'МО',
            'latitude': '11.11111',
            'longitude': '22.22222'
        }
        response = self.client.put(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['city'], data['city'])
        self.assertEqual(response.data['zip_code'], data['zip_code'])

    def test_delete_location(self):
        """
        Тест возможности удаления локации.
        """
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
