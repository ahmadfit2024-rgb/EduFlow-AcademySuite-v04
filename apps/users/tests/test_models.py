from django.test import TestCase
from apps.users.models import CustomUser

class CustomUserModelTest(TestCase):
    
    def test_user_creation(self):
        """
        Tests that a user can be created with a specific role.
        """
        user = CustomUser.objects.create_user(
            username='teststudent',
            email='student@example.com',
            password='password123',
            role=CustomUser.Roles.STUDENT
        )
        self.assertEqual(user.username, 'teststudent')
        self.assertEqual(user.role, 'student')
        self.assertTrue(user.check_password('password123'))