from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from apps.users.models import CustomUser

class UserAPITest(APITestCase):

    def setUp(self):
        # Create an admin user for testing restricted endpoints
        self.admin_user = CustomUser.objects.create_user(
            username='adminuser',
            password='password123',
            role=CustomUser.Roles.ADMIN,
            is_staff=True,
            is_superuser=True
        )

    def test_unauthorized_user_list(self):
        """
        Ensure unauthenticated users cannot access the user list API.
        """
        url = reverse('user-list') # Assumes the URL name is 'user-list'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)