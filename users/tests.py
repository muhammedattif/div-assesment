from django.test import TestCase, Client
from rest_framework.test import APIClient, APITestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from users.models import User

class UserTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()

        # HTTP_AUTHORIZATION in the header
        self.client.credentials(HTTP_AUTHORIZATION='Token ada7f3a9ce51edab5ad44478ffe3c5bd46cbf492')

        self.create_user_url = reverse('users-api:user-create')
        self.auth_token_url = reverse('users-api:auth-token')
        self.create_status_url = reverse('users-api:status-create')


    def test_create_user(self):

        # read the image from the disk

        image = open('test.png')
        response = self.client.post(self.create_user_url, {
                'phone_number': "+201020404058",
                'first_name': 'test',
                'last_name': 'test',
                'country_code': 'eg',
                'email': 'test@test.com',
                'birth_date': '1999-12-12',
                'gender': 'male',
                'avatar': image
        })

        self.assertEquals(response.status_code, 201)

    def test_get_auth_token(self):
        response = self.client.post(self.auth_token_url, {
                'phone_number': "+20123456789",
                'password': 'test'
        })
        self.assertEquals(response.status_code, 200)


    def test_create_status_object(self):

        response = self.client.post(self.create_status_url, {
                'phone_number': "+20123456789",
                'status': 'status1'
        })
        self.assertEquals(response.status_code, 201)
