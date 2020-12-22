from core.permissions import PERDANA_USER_ROLE
from django.contrib.auth.models import Group
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = "Command for init groups member"

    def handle(self, *args, **options):
        for role in PERDANA_USER_ROLE:
            group, _ = Group.objects.get_or_create(name=role)
            print("Group %s created!" % group.name)
