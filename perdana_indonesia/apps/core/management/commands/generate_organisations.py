from club.models import Club
from core.choices import CLUB_UNIT_TYPE_CHOICES
from django.core.management import BaseCommand
from region.models import Kelurahan, Regional


class Command(BaseCommand):
    help = "Command for generate initial organisations"
    initialClubs = [
        {
            'name': 'Arrihu Archery',
            'address': 'Mataram',
            'central': None,
            'organisation_id': 'PERDANA-CLUB-97987239872',
            'date_register': '2019-05-29',
            'org_type': CLUB_UNIT_TYPE_CHOICES[0][0],
            'village_code': '52_71_1_1008'
        },
        {
            'name': 'Damu Archery',
            'organisation_id': 'PERDANA-CLUB-97987239875',
            'central': 'PERDANA-97987239872',
            'address': 'Ampenan',
            'date_register': '2019-07-29',
            'org_type': CLUB_UNIT_TYPE_CHOICES[0][0],
            'village_code': '52_71_1_1004'
        },
        {
            'name': 'SD IT Mataram',
            'organisation_id': 'PERDANA-UNIT-97987239888',
            'central': None,
            'address': 'Mataram',
            'date_register': '2019-07-29',
            'org_type': CLUB_UNIT_TYPE_CHOICES[1][0],
            'village_code': '52_71_2_1001'
        }
    ]

    def getClubCentralOrNone(self, centralOrganisationId) -> Club:
        if not centralOrganisationId:
            return None
            
        try:
            return Club.objects.get(organisation_id=centralOrganisationId)
        except Club.DoesNotExist:
            return None

    def getVillage(self, code) -> Kelurahan:
        return Kelurahan.objects.get(code=code)

    def handle(self, *args, **options):
        for clubData in self.initialClubs:
            instance, _ = Club.objects.get_or_create(
                organisation_id=clubData.get('organisation_id')
            )
            instance.name = clubData.get('name')
            instance.central = self.getClubCentralOrNone(clubData.get('central'))
            instance.address = clubData.get('address')
            instance.org_type = clubData.get('org_type')
            instance.date_register = clubData.get('date_register')
            instance.village = self.getVillage(clubData.get('village_code'))
            instance.save()

            print('Processing %s' % instance.name)
