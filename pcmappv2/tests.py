from django.test import TestCase
from django.test import Client
# Create your tests here.

class ProjectTests(TestCase):

    def test_homepage(self):
        response = self.client.get('/pcmappv2/')
        self.assertEqual(response.status_code, 200)

    def test_baseredirect(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code,302)

    def test_baseredirect_with_oldurl(self):
        response=self.client.get('/pcmapp/')
        self.assertEqual(response.status_code,302)

class MemberRegistrationTests(TestCase):

    def test_registration_pageload(self):
        response = self.client.get('/pcmappv2/register/')
        self.assertEqual(response.status_code,200)
