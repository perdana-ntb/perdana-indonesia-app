from django.core.management import BaseCommand
from orm import region as region_models, club as club_models


class Command(BaseCommand):
    help = "Command for generate initial organisations"
    initial_regions = [{'name': 'Indonesia Timur'}, {'name': 'Indonesia Tengah'}]
    initial_provinces = [{'name': 'Nusa Tenggara Barat'}, {'name': 'Nusa Tenggara Timur'}]
    initial_branchs = [{'name': 'Mataram'}, {'name': 'Lombok Tengah'}, {'name': 'Lombok Barat'}, {'name': 'Lombok Timur'}]
    initial_clubs = [{'name': 'Arrihu Archery', 'address': 'Mataram', 'date_register': '2019-05-29'},
                     {'name': 'Damu Archery', 'address': 'Ampenan', 'date_register': '2019-07-29'}]
    initial_unit = {'name': 'SD IT Mataram', 'address': 'Mataram', 'date_register': '2019-07-29'}

    def handle(self, *args, **options):
        self.stdout.write("Started . . .")
        for region in self.initial_regions:
            region_models.Region.objects.create(**region)
        
        regional = region_models.Region.objects.get(name=self.initial_regions[0]['name'])
        for province in self.initial_provinces:
            region_models.Province.objects.create(**province, regional=regional)

        province = region_models.Province.objects.get(name=self.initial_provinces[0]['name'])
        for branch in self.initial_branchs:
            club_models.Branch.objects.create(**branch, province=province)

        branch = club_models.Branch.objects.get(name=self.initial_branchs[0]['name'])
        for club in self.initial_clubs:
            club_models.Club.objects.create(**club, branch=branch)

        club_models.Unit.objects.create(**self.initial_unit, branch=branch)
        self.stdout.write("Finished . . .")
