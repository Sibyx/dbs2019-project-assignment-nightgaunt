import csv
from pathlib import Path
from typing import OrderedDict

from django.core.management import BaseCommand, CommandError

from core.models import TaxonomicKingdom, TaxonomicPhylum, TaxonomicClass, TaxonomicOrder, TaxonomicFamily, TaxonomicGenus, TaxonomicSpecies, TaxonomicSubspecies, Organism


class Command(BaseCommand):
    help = 'Import species from Species+ catalog'

    def add_arguments(self, parser):
        parser.add_argument('--file', nargs='?', type=str, help="Path to Species+ CSV file", required=True)

    def handle(self, *args, **options):
        if not Path(options['file']).is_file():
            raise CommandError("Input file does not exist!")

        with open(options['file']) as csv_file:
            reader = csv.DictReader(csv_file, delimiter=';')

            for row in reader:
                self._insert_record(row)

    def _insert_record(self, row: OrderedDict):
        # Kingdom
        taxonomic_kingdom, created = TaxonomicKingdom.objects.get_or_create(
            name=row['Kingdom']
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"Imported kingdom: {taxonomic_kingdom}"))

        # Phylum
        taxonomic_phylum, created = TaxonomicPhylum.objects.get_or_create(
            name=row['Phylum'],
            kingdom=taxonomic_kingdom
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"Imported phylum: {taxonomic_phylum}"))

        # Class
        taxonomic_class, created = TaxonomicClass.objects.get_or_create(
            name=row['Class'],
            taxonomic_phylum=taxonomic_phylum
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"Imported class: {taxonomic_class}"))

        # Order
        taxonomic_order, created = TaxonomicOrder.objects.get_or_create(
            name=row['Order'],
            taxonomic_class=taxonomic_class
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"Imported order: {taxonomic_order}"))

        # Family
        taxonomic_family, created = TaxonomicFamily.objects.get_or_create(
            name=row['Family'],
            taxonomic_order=taxonomic_order
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"Imported family: {taxonomic_family}"))

        # Genus
        taxonomic_genus, created = TaxonomicGenus.objects.get_or_create(
            name=row['Genus'],
            taxonomic_family=taxonomic_family
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"Imported genus: {taxonomic_genus}"))

        # Species
        taxonomic_species, created = TaxonomicSpecies.objects.get_or_create(
            name=row['Species'],
            taxonomic_genus=taxonomic_genus
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"Imported species: {taxonomic_species}"))

        # Subspecies
        if row['Subspecies'].strip():
            taxonomic_subspecies, created = TaxonomicSubspecies.objects.get_or_create(
                name=row['Subspecies'],
                taxonomic_species=taxonomic_species
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Imported species: {taxonomic_subspecies}"))
        else:
            taxonomic_subspecies = None

        try:
            Organism.objects.get(
                taxonomic_species=taxonomic_species,
                taxonomic_subspecies=taxonomic_subspecies,
                name=row['Scientific Name']
            )
        except Organism.DoesNotExist:
            """
            Possible author formats:
            - Rauh & Backeberg, 1957: OK
            - Backeberg: OK
            - (Kunth) Backeberg ex A.W.Hill: OK
            - (L.f.) Sweet 1830
            - H. Perrier 1944
            - (Naumov, 1960): OK
            - Fisher, Harlow, Edwards & Keogh 2008
            """
            if row['Author'].strip():
                prepared_string = row['Author'].strip()
                if (prepared_string[0] == '(') and (prepared_string[-1] == ')'):
                    prepared_string = prepared_string[1:-1]
                author_bits = prepared_string.split(',')

                if len(author_bits) == 1:
                    if author_bits[0].isdigit():
                        year = author_bits[0].strip()
                        author = None
                    else:
                        year = None
                        author = author_bits[0].strip()
                else:
                    # FIXME: year without comma separator (check for number in string), maybe regex
                    year = author_bits[-1].strip().translate({ord(c): None for c in '()'})
                    author = ','.join(author_bits[0:-1]).strip()
            else:
                author = None
                year = None
            organism = Organism.objects.create(
                name=row['Scientific Name'],
                author=author,
                year=year,
                taxonomic_species=taxonomic_species,
                taxonomic_subspecies=taxonomic_subspecies
            )
            self.stdout.write(self.style.SUCCESS(f"Imported organism: {organism}"))
