import io

import random
import shutil
import uuid

from dateutil.tz import tz
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.management import BaseCommand
from django.db import IntegrityError
from faker import Faker
from faker.providers import lorem, date_time
from robohash import Robohash

from core.models import Box, User, Specimen, Organism, Photo
from importer.providers.plant import PlantProvider
from importer.providers.specimen import SpecimenProvider


class Command(BaseCommand):

    def __init__(self, stdout=None, stderr=None, no_color=False, force_color=False):
        super().__init__(stdout, stderr, no_color, force_color)

        self.faker = Faker()
        self.faker.add_provider(PlantProvider)
        self.faker.add_provider(lorem)
        self.faker.add_provider(date_time)
        self.faker.add_provider(SpecimenProvider)

        self.creator = User.objects.first()

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear collection before faking new data'
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write(self.style.WARNING("Clearing database"))
            Box.objects.hard_delete()
            self.stdout.write(self.style.WARNING("Removing related files"))
            shutil.rmtree(f"{settings.MEDIA_ROOT}/photos")

        self.stdout.write("Generating objects")
        for index in range(settings.DEMONSTRATION['BOXES']):
            box = self._generate_box()
            self.stdout.write(f"[{index:5d} / {settings.DEMONSTRATION['BOXES']:5d}] {box.title}")

        self.stdout.write(self.style.SUCCESS('Finished'))

    def _generate_box(self) -> Box:
        try:
            box = Box.objects.create(
                title=self.faker.plant_family(),
                description=self.faker.paragraph(),
                creator=self.creator
            )

            i = random.randint(
                settings.DEMONSTRATION['SPECIMENS']['MIN'],
                settings.DEMONSTRATION['SPECIMENS']['MAX'],
            )

            for _ in range(i):
                self._generate_specimen(box)

            return box
        except IntegrityError:
            return self._generate_box()

    def _generate_specimen(self, box: Box):
        specimen = Specimen.objects.create(
            creator=self.creator,
            organism=Organism.objects.random(),
            box=box,
            gender=self.faker.specimen_gender(),
            form=self.faker.specimen_form(),
            happened_at=self.faker.date_time_between(start_date="-40y", end_date="now", tzinfo=tz.gettz('UTC')),
            notes=self.faker.paragraph(),
            dna=self.faker.sentence()
        )

        for _ in range(settings.DEMONSTRATION['PHOTOS']):
            self._generate_photo(specimen)

    def _generate_photo(self, specimen: Specimen):
        filename = f'{str(uuid.uuid4())}.png'
        data = io.BytesIO()

        rh = Robohash(filename)
        rh.assemble(roboset='any', sizex=1024, sizey=1024)
        rh.img.save(data, format='PNG')

        file = InMemoryUploadedFile(data, None, filename, 'image/png', rh.img.size, None)

        photo = Photo(
            specimen=specimen,
            creator=self.creator,
            title=self.faker.sentence(),
            mime='image/png',
            happened_at=self.faker.date_time_between(start_date="-40y", end_date="now", tzinfo=tz.gettz('UTC')),
            description=self.faker.paragraph()
        )

        photo.path.save(filename, file)
        photo.save()
