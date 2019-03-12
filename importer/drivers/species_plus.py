import csv
from typing import OrderedDict, Tuple, Union

from core.models import TaxonomicKingdom, TaxonomicPhylum, TaxonomicClass, TaxonomicOrder, TaxonomicFamily, \
    TaxonomicGenus, TaxonomicSpecies, TaxonomicSubspecies, Organism


class SpeciesPlus(object):
    DRIVER_NAME = 'species_plus'

    def __init__(self, file: str):
        self._counters = {
            'Kingdoms': 0,
            'Phylums': 0,
            'Classes': 0,
            'Orders': 0,
            'Families': 0,
            'Genuses': 0,
            'Species': 0,
            'Subspecies': 0,
            'Organisms': 0
        }
        self._file = file

    def execute(self):
        with open(self._file) as csv_file:
            reader = csv.DictReader(csv_file, delimiter=';')

            for row in reader:
                self._insert_record(row)

        return self._counters

    def _insert_record(self, row: OrderedDict):
        # Kingdom
        taxonomic_kingdom, created = TaxonomicKingdom.objects.get_or_create(
            name=row['Kingdom']
        )
        if created:
            self._counters['Kingdoms'] += 1

        # Phylum
        taxonomic_phylum, created = TaxonomicPhylum.objects.get_or_create(
            name=row['Phylum'],
            kingdom=taxonomic_kingdom
        )
        if created:
            self._counters['Phylums'] += 1

        # Class
        taxonomic_class, created = TaxonomicClass.objects.get_or_create(
            name=row['Class'],
            taxonomic_phylum=taxonomic_phylum
        )
        if created:
            self._counters['Classes'] += 1

        # Order
        taxonomic_order, created = TaxonomicOrder.objects.get_or_create(
            name=row['Order'],
            taxonomic_class=taxonomic_class
        )
        if created:
            self._counters['Orders'] += 1

        # Family
        taxonomic_family, created = TaxonomicFamily.objects.get_or_create(
            name=row['Family'],
            taxonomic_order=taxonomic_order
        )
        if created:
            self._counters['Families'] += 1

        # Genus
        taxonomic_genus, created = TaxonomicGenus.objects.get_or_create(
            name=row['Genus'],
            taxonomic_family=taxonomic_family
        )
        if created:
            self._counters['Genuses'] += 1

        # Species
        taxonomic_species, created = TaxonomicSpecies.objects.get_or_create(
            name=row['Species'],
            taxonomic_genus=taxonomic_genus
        )
        if created:
            self._counters['Species'] += 1

        # Subspecies
        if row['Subspecies'].strip():
            taxonomic_subspecies, created = TaxonomicSubspecies.objects.get_or_create(
                name=row['Subspecies'],
                taxonomic_species=taxonomic_species
            )
            if created:
                self._counters['Subspecies'] += 1
        else:
            taxonomic_subspecies = None

        try:
            Organism.objects.get(
                taxonomic_species=taxonomic_species,
                taxonomic_subspecies=taxonomic_subspecies,
                name=row['Scientific Name']
            )
        except Organism.DoesNotExist:
            author, year = self._parse_author(row['Author'])
            Organism.objects.create(
                name=row['Scientific Name'],
                author=author,
                year=year,
                taxonomic_species=taxonomic_species,
                taxonomic_subspecies=taxonomic_subspecies
            )
            self._counters['Organisms'] += 1

    def _parse_author(self, raw_input: str) -> Tuple[Union[str, None], Union[str, None]]:
        """
        Possible author formats:
        - Rauh & Backeberg, 1957: OK
        - Backeberg: OK
        - (Kunth) Backeberg ex A.W.Hill: OK
        - (L.f.) Sweet 1830: OK
        - H. Perrier 1944: OK
        - (Naumov, 1960): OK
        - Fisher, Harlow, Edwards & Keogh 2008: OK
        """
        raw_input = raw_input.strip()

        if not raw_input:
            return None, None

        # 1. Remove braces if there are from both sides
        if (raw_input[0] == '(') and (raw_input[-1] == ')'):
            raw_input = raw_input[1:-1]

        # 2.Try to extract year using space separator
        bits = raw_input.split(' ')
        if bits[-1].isdigit():
            return ' '.join(bits[0:-1]).strip('').strip(','), bits[-1].strip()

        # 3. Try to extract using comma
        bits = raw_input.split(',')

        if len(bits) == 1:
            if bits[0].isdigit():
                return None, bits[0].strip()
            else:
                return bits[0].strip(), None

        return raw_input, None
