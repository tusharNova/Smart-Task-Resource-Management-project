from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework import status


User= get_user_model()

class ProjectAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tushar', password='1234')
        token_resp = self.client.post(reverse('token_obtain_pair'), {'username':'tushar','password':'1234'}, format='json')
        self.access = token_resp.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access}')


    def test_create_and_list_project(self):
        resp = self.client.post('/api/projects/', {'name':'API Project', 'description':'desc'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        list_resp = self.client.get('/api/projects/')
        self.assertEqual(list_resp.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(list_resp.data['results']), 1)