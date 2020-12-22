from django.urls import reverse
from django.utils import timezone
from model_mommy import mommy
from rest_framework import status
from rest_framework.test import APITestCase

from club.models import ArcheryRange
from core import logger
from core.tests import TestMixins
from practice.models import PracticeSchedule
from practice.viewsets import NearestPracticeViewSet


class NearestPracticeViewSetApiTestCase(TestMixins, APITestCase):
    user_location = "-8.5827968,116.1186189"

    def add_time(self, diff):
        return timezone.now() + timezone.timedelta(minutes=10)

    def sub_time(self, diff):
        return timezone.now() - timezone.timedelta(minutes=10)

    def setUp(self):
        self.create_user_gruops()
        self.create_archer_user()

        self.archery_range1 = mommy.make(ArcheryRange, name="Sri Coffe",
                                         latitude=-8.5839641, longitude=116.0741541)
        self.archery_range2 = mommy.make(ArcheryRange, name="Lapangan Golf Pelembak",
                                         latitude=-8.565878, longitude=116.0840576)

        self.schedule1 = mommy.make(PracticeSchedule, archery_range=self.archery_range1,
                                    day=1, fullday=True, start_time=self.sub_time(10),
                                    end_time=self.add_time(60))
        self.schedule2 = mommy.make(PracticeSchedule, archery_range=self.archery_range2,
                                    day=timezone.now().weekday(), fullday=False,
                                    start_time=self.sub_time(10), end_time=self.add_time(60))

    def test_fetch_nearest_practice_without_auth_should_return_401(self):
        url = reverse('practice_api:nearest-practices-list')
        r = self.client.get(url)
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_fetch_nearest_practice_authorized_should_return_all_schedule(self):
        self.auth(username="archer2")
        url = '%s?query_type=%s&coordinate=%s' % (
            reverse('practice_api:nearest-practices-list'),
            NearestPracticeViewSet.NEAREST_PRACTICE_CHOICES[0],
            self.user_location
        )
        r = self.client.get(url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        results = r.json().get('results')

        self.assertEqual(len(results), 2)

    def test_fetch_nearest_practice_authorized_should_return_open_schedule(self):
        self.auth(username="archer2")
        url = '%s?query_type=%s&coordinate=%s' % (
            reverse('practice_api:nearest-practices-list'),
            NearestPracticeViewSet.NEAREST_PRACTICE_CHOICES[1],
            self.user_location
        )
        r = self.client.get(url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        results = r.json().get('results')

        self.assertEqual(len(results), 1)
