from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from .factories import LocationFactory, CargoFactory
from transport.models import Cargo


class CargoAPITestCase(APITestCase):

    def setUp(self):
        self.pickup_location = LocationFactory()
        self.delivery_location = LocationFactory()
        self.cargo = CargoFactory()
        self.list_url = reverse('cargo-list')
        self.detail_url = reverse('cargo-detail', args=[self.cargo.id])

    def test_create_cargo(self):
        """
        Тест возможности создания груза.
        """
        data = {
            'pickup_location_zip': self.pickup_location.zip_code,
            'delivery_location_zip': self.delivery_location.zip_code,
            'weight': 200,
            'description': 'Описание'
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_cargo(self):
        """
        Тест возможности получения списка грузов.
        """
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_cargo(self):
        """
        Тест возможности изменения груза.
        """
        data = {
            'description': 'Новое описание',
            'weight': 300,
            'pickup_location_zip': self.pickup_location.zip_code,
            'delivery_location_zip': self.delivery_location.zip_code,
        }
        response = self.client.put(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], data['description'])

    def test_delete_cargo(self):
        """
        Тест возможности удаления груза.
        """
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
