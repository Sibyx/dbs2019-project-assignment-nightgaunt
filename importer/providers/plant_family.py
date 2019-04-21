import csv
import random

from django.conf import settings

from faker.providers import BaseProvider


class PlantFamilyProvider(BaseProvider):

    def __init__(self, generator):
        super().__init__(generator)

        self.dataset = {
            'plant_families': []
        }

        with open(f'{settings.BASE_DIR}/importer/assets/plant_families.csv') as csv_file:
            reader = csv.reader(csv_file, delimiter=',')

            for row in reader:
                self.dataset['plant_families'].append(row[0])

    def plant_family(self) -> str:
        return f"{random.choice(self.dataset.get('plant_families', []))} {random.randint(1, 42)}"
