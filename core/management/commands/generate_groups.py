from django.core.management import BaseCommand
from core.permissions import PERDANA_USER_ROLE
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = "Command for init groups member"

    def handle(self, *args, **options):
        for role in PERDANA_USER_ROLE:
            try:
                group = Group.objects.get(name=role)
                group.name = role
                group.save()
            except Group.DoesNotExist:
                group = Group.objects.create(name=role)
                
            self.stdout.write("Group %s created!" % group.name)