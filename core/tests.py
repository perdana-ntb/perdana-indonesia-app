
from io import BytesIO

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.urls import reverse
from model_mommy import mommy
from PIL import Image
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

# Create your tests here.
from core.permissions import PERDANA_USER_ROLE
from orm.models import club as club_models
from orm.models import commite as commite_models
from orm.models import member as member_models
from orm.models import region as region_models

USER = get_user_model()


class TestMixins:
    def create_user_gruops(self):
        self.regional_group = Group.objects.create(name=PERDANA_USER_ROLE[0])
        self.pengprov_group = Group.objects.create(name=PERDANA_USER_ROLE[1])
        self.pengcab_group = Group.objects.create(name=PERDANA_USER_ROLE[2])
        self.club_or_unit_group = Group.objects.create(name=PERDANA_USER_ROLE[3])
        self.archer_group = Group.objects.create(name=PERDANA_USER_ROLE[4])

    def create_archer_user(self):
        self.user1 = USER.objects.create_user(username='archer1', password='123')
        self.user1.groups.add(self.archer_group)
        Token.objects.create(user=self.user1)
        self.archer_member1 = mommy.make(member_models.ArcherMember, user=self.user1)

        self.user2 = USER.objects.create_user(username='archer2', password='123')
        self.user2.groups.add(self.archer_group)
        Token.objects.create(user=self.user2)
        self.archer_member2 = mommy.make(member_models.ArcherMember, user=self.user2, approved=True)

    def auth(self, username, password='123'):
        auth_url = reverse('member_api:login')
        data = {
            'username': username, 'password': password
        }
        response = self.client.post(auth_url, data, format='json')
        if (str(response.status_code).startswith('20')):
            self.token = response.json().get('token')
            self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        return response

    def generate_file(self):
        file = BytesIO()
        image = Image.new('RGBA', size=(50, 50), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        return file


class AuthTestCase(APITestCase, TestMixins):
    def setUp(self):
        self.create_user_gruops()
        self.create_archer_user()

    def test_archer_auth(self):
        r = self.auth('archer2', '123')
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in r.json())
        self.assertEqual(r.json()['role'], PERDANA_USER_ROLE[4])

    def test_archer_auth_not_approved(self):
        r = self.auth('archer1', '123')
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)

    def test_auth_wrong_password(self):
        r = self.auth('archer1', '')
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
