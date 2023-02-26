
from rest_framework.test import APITestCase
from django.urls import reverse


#Install faker to generate random data instead of manually inputting the data

class TestSetUp(APITestCase):

   def setUp(self):
      self.register_url = reverse('register')
      self.login_url=reverse('login')

      self.user_data = {
         'email': 'email@email.com',
         'username': 'email',
         'password': 'email@email.com'
      }
      return super().setUp()

   def tearDown(self):
      return super().tearDown()