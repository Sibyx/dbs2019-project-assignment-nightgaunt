from pathlib import Path

from django.core.management import BaseCommand, CommandError

from importer.drivers.species_plus import SpeciesPlus


class Command(BaseCommand):
    help = 'Import species from Species+ catalog'

    def add_arguments(self, parser):
        parser.add_argument('--file', nargs='?', type=str, help="Path to Species+ CSV file", required=True)
        parser.add_argument('--driver', nargs='?', type=str, help="Import driver", default='species_plus')

    def handle(self, *args, **options):
        if not Path(options['file']).is_file():
            raise CommandError("Input file does not exist!")

        if options['driver'] is SpeciesPlus.DRIVER_NAME:
            driver = SpeciesPlus(options['file'])
        else:
            raise CommandError(f"Invalid import driver: {options['driver']}")

        counters = driver.execute()

        self.stdout.write("Imported:")
        for (index, value) in counters.items():
            self.stdout.write(f"\t{index}: {value}")
