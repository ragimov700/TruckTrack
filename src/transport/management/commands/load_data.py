import csv
import os

from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import IntegrityError

from transport.models import Location


class Command(BaseCommand):
    """
    Команда для массовой загрузки данных локаций и грузовиков в базу данных.
    """
    help = 'Массовая загрузка данных локаций и грузовиков.'

    def handle(self, *args, **kwargs):
        self.load_locations()
        self.load_trucks()

    def load_locations(self):
        file_path = os.path.join('data', 'locations.csv')
        try:
            with open(file_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                locations = []
                BATCH_SIZE = 1000

                for row in reader:
                    location = Location(
                        city=row['city'],
                        state=row['state_id'],
                        zip_code=row['zip'],
                        latitude=row['lat'],
                        longitude=row['lng']
                    )
                    locations.append(location)

                    if len(locations) >= BATCH_SIZE:
                        Location.objects.bulk_create(locations)
                        locations.clear()

                if locations:
                    Location.objects.bulk_create(locations)
        except IntegrityError:
            self.stdout.write(self.style.ERROR(
                'Произошла ошибка при загрузке локаций: локации уже загружены'
            ))
        else:
            self.stdout.write(self.style.SUCCESS(
                'Локации успешно загружены в базу данных'
            ))

    def load_trucks(self):
        try:
            call_command('loaddata', 'data/trucks.json')
            self.stdout.write(self.style.SUCCESS(
                'Грузовики успешно загружены из фикстуры в базу данных'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(
                f'Произошла ошибка при загрузке грузовиков: {e}'))
