import random

from faker.providers import BaseProvider

from core.models.specimen import GenderChoice


class SpecimenProvider(BaseProvider):

    def specimen_gender(self) -> GenderChoice:
        return random.choice(list(GenderChoice)).value

    def specimen_form(self) -> str:
        forms = ['Super', 'Average', 'Funny', 'Weird', 'Satanic', 'Alien', 'Stinky']
        return random.choice(forms)
