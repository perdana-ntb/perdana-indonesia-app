from django.contrib.auth import get_user_model
from django.urls import reverse
from model_mommy import mommy
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from core.tests import TestMixins
from orm.models import club as club_models
from orm.models import commite as commite_models
from orm.models import member as member_models
from orm.models import region as region_models

USER = get_user_model()


class ArcherMemberListTestCase(TestMixins, APITestCase):
    url = reverse('user_api:member-list')

    def setUp(self):
        self.create_user_gruops()

        self.region1 = mommy.make(region_models.Region)
        self.region2 = mommy.make(region_models.Region)

        self.province1 = mommy.make(region_models.Province, regional=self.region1)
        self.province2 = mommy.make(region_models.Province, regional=self.region2)

        self.branch1 = mommy.make(club_models.Branch, province=self.province1)
        self.branch2 = mommy.make(club_models.Branch, province=self.province2)

        self.club1 = mommy.make(club_models.Club, branch=self.branch1)
        self.club2 = mommy.make(club_models.Club, branch=self.branch2)

        self.satuan1 = mommy.make(club_models.Unit, branch=self.branch1)
        self.satuan2 = mommy.make(club_models.Unit, branch=self.branch2)

        self.members_club1 = mommy.make(member_models.ArcherMember, _quantity=8, club=self.club1, approved=True)
        self.members_club2 = mommy.make(member_models.ArcherMember, _quantity=9, club=self.club2, approved=True)

        self.members_satuan1 = mommy.make(member_models.ArcherMember, _quantity=5, satuan=self.satuan1, approved=True)
        self.members_satuan2 = mommy.make(member_models.ArcherMember, _quantity=6, satuan=self.satuan2, approved=True)

    def create_regional_user(self):
        self.regional_user = USER.objects.create_user(username='regional1', password='123')
        self.regional_user.groups.add(self.regional_group)
        Token.objects.create(user=self.regional_user)
        self.regional_member = mommy.make(commite_models.RegionalCommiteMember, user=self.regional_user, regional=self.region1)

    def test_fetch_member_list_by_regional(self):
        self.create_regional_user()
        self.auth(username='regional1')

        r = self.client.get(self.url)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()['results']), 13)
