from django.core.management import BaseCommand

from club.models import Branch, ClubUnit
from region.models import Province, Region


class Command(BaseCommand):
    help = "Command for generate initial organisations"
    initial_regions = [
        {'name': 'Indonesia Timur'}, {'name': 'Indonesia Tengah'}
    ]
    initial_provinces = [
        {'name': 'Nusa Tenggara Barat'}, {'name': 'Nusa Tenggara Timur'}
    ]
    initial_branchs = [
        {'name': 'Mataram'}, {'name': 'Lombok Tengah'},
        {'name': 'Lombok Barat'}, {'name': 'Lombok Timur'}
    ]
    initial_clubunits = [
        {'name': 'Arrihu Archery', 'address': 'Mataram',
         'date_register': '2019-05-29', 'type': ClubUnit.CLUB_UNIT_TYPE_CHOICES[0][0]},
        {'name': 'Damu Archery', 'address': 'Ampenan',
         'date_register': '2019-07-29', 'type': ClubUnit.CLUB_UNIT_TYPE_CHOICES[0][0]},
        {'name': 'SD IT Mataram', 'address': 'Mataram',
         'date_register': '2019-07-29', 'type': ClubUnit.CLUB_UNIT_TYPE_CHOICES[1][0]}
    ]

    def handle(self, *args, **options):
        self.stdout.write("Started . . .")
        for region in self.initial_regions:
            Region.objects.create(**region)

        regional = Region.objects.get(name=self.initial_regions[0]['name'])
        for province_data in self.initial_provinces:
            Province.objects.create(**province_data, regional=regional)

        province = Province.objects.get(name=self.initial_provinces[0]['name'])
        for branch_data in self.initial_branchs:
            Branch.objects.create(**branch_data, province=province)

        branch = Branch.objects.get(name=self.initial_branchs[0]['name'])
        for clubunit_data in self.initial_clubunits:
            ClubUnit.objects.create(**clubunit_data, branch=branch)

        self.stdout.write("Finished . . .")
