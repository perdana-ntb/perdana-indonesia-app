
import os

from core.dataframe import DataframeUtil
from django.conf import settings
from django.core.management import BaseCommand
from region.models import Kabupaten, Kecamatan, Kelurahan, Provinsi


class Command(BaseCommand):
    help = "Command for generate initial organisations"
    regionFiles = (
        # (Mdodel, Dependency, Filename)
        (Provinsi, None, 'Provinsi.xlsx'),
        (Kabupaten, Provinsi, 'Kabupaten.xlsx'),
        (Kecamatan, Kabupaten, 'Kecamatan.xlsx'),
        (Kelurahan, Kecamatan, 'Kelurahan.xlsx')
    )
    staticPath = os.path.join(settings.BASE_DIR, 'static/docs/regions')

    def getParentOrNone(self, parentModel, code):
        if not parentModel:
            return None

        try:
            return parentModel.objects.get(code=code)
        except parentModel.DoesNotExist:
            return None

    def insertRegionIntoDatabase(self, model, parentModel, rowData: dict):
        parent = self.getParentOrNone(parentModel, rowData.get('parent'))
        instance, _ = model.objects.get_or_create(
            code=rowData.get('code'), name=rowData.get('name')
        )
        if isinstance(instance, Provinsi):
            instance.code_name = rowData.get('codename')
        else:
            exec("instance.{0}_id = {1}".format(parentModel.__name__.lower(), parent))
        instance.save()

    def handle(self, *args, **options):
        for region in self.regionFiles:
            regionPath = os.path.join(self.staticPath, region[2])
            dataframe = DataframeUtil.getValidatedDataframe(regionPath)
            for index, row in dataframe.iterrows():
                self.insertRegionIntoDatabase(region[0], region[1], row)
                print('Processing %s at row %s' % (region[0].__name__, index + 1))

        print('Process Completed!')
