from django.conf import settings
from django.core.management import BaseCommand
from django.db import IntegrityError
from faker import Faker
from faker.providers import lorem

from core.models import Box, User
from importer.providers.plant_family import PlantFamilyProvider


class Command(BaseCommand):

    def __init__(self, stdout=None, stderr=None, no_color=False, force_color=False):
        super().__init__(stdout, stderr, no_color, force_color)

        self.faker = Faker()
        self.faker.add_provider(PlantFamilyProvider)
        self.faker.add_provider(lorem)

        self.creator = User.objects.first()

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear collection before faking new data'
        )

    def handle(self, *args, **options):
        if options['clear']:
            Box.objects.hard_delete()

        for _ in range(settings.DEMONSTRATION['BOXES']):
            self._generate_box()

    def _generate_box(self):
        try:
            box = Box.objects.create(
                title=self.faker.plant_family(),
                description=self.faker.paragraph(),
                creator=self.creator
            )

            self.stdout.write(f"{box.title}: {box.description}", ending='\n')
        except IntegrityError:
            self._generate_box()
