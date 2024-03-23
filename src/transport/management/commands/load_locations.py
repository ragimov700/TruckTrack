import csv
import os
from django.core.management.base import BaseCommand
from transport.models import Location


class Command(BaseCommand):
    """
    Команда для массовой загрузки данных локаций из файла CSV в базу данных.
    """
    help = 'Массовая загрузка локаций из файла CSV'

    def handle(self, *args, **kwargs):
        file_path = os.path.join('data', 'locations.csv')
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

        self.stdout.write(self.style.SUCCESS(
            'Локации успешно загружены в базу данных'
        ))
