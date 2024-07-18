from unittest.mock import Mock, patch, MagicMock

from django.db.models import QuerySet
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from apps.projects.models import Project
from apps.users.models import User
from apps.users.serializers import UserListSerializer, RegisterUserSerializer
from django.urls import reverse

from apps.users.views import UserListGenericView


class TestUserEndpoints(APITestCase):

    fixtures = ['apps/fixtures/users_fixture.json', 'apps/fixtures/projects_fixture.json']

    def setUp(self):
        self.client = APIClient()
        self.project1 = Project.objects.get(pk=1)
        self.project2 = Project.objects.get(pk=2)
        self.user1 = User.objects.get(pk=1)
        self.user1.project = self.project1
        self.user1.save()
        self.user2 = User.objects.get(pk=2)
        self.user2.project = self.project2
        self.user2.save()
        self.get_users = reverse('user-list')
        self.get_users_by_project_name = reverse('user-list') + '?project_name=' + self.project1.name
        self.register_user = reverse('register-user')

    @patch.object(
        target=UserListGenericView,
        attribute='get_queryset',
    )
    def test_get_all_users(self, mock_get_object):
        users = [self.user1, self.user2]

        mock_queryset = MagicMock(spec=QuerySet)
        mock_queryset.__iter__.return_value = iter(users)
        mock_get_object.return_value = mock_queryset

        response = self.client.get(self.get_users)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer = UserListSerializer(users, many=True)
        self.assertEqual(response.data, serializer.data)

    @patch.object(
        target=UserListGenericView,
        attribute='get_queryset',
    )
    def test_get_users_by_project_name(self, mock_get_object):
        user_by_project_name = [self.user1]

        mock_queryset = MagicMock(spec=QuerySet)
        mock_queryset.__iter__.return_value = iter([self.user2])
        mock_get_object.return_value = mock_queryset

        response = self.client.get(self.get_users_by_project_name)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer = UserListSerializer(user_by_project_name, many=True)
        self.assertEqual(response.data, serializer.data)

    @patch.object(
        target=UserListGenericView,
        attribute='get_queryset',
    )
    def test_get_empty_user_list(self, mock_get_object):
            mock_queryset = MagicMock(spec=QuerySet)
            mock_queryset.exists.return_value = False
            mock_get_object.return_value = mock_queryset

            response = self.client.get(self.get_users)
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

            self.assertFalse(response.data)

    def test_create_user_valid_data(self):
        valid_payload = {
            "username": "testuser_create",
            "first_name": "Testcreate",
            "last_name": "Usercreate",
            "email": "test_create@example.com",
            "position": "CEO",
            "password": "SuperSecurePassword1234!",
            "re_password": "SuperSecurePassword1234!"

        }
        response = self.client.post(self.register_user, valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertTrue(User.objects.filter(username='testuser_create').exists())

    def test_create_user_invalid_data(self):
        invalid_payload = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'invalidemail',
            'position': 'Developer',
            'password': 'password123',
            're_password': 'password123'
        }
        response = self.client.post(self.register_user, invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_missing_required_fields(self):
        missing_required_fields_payload = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'password': 'securepassword',
            're_password': 'securepassword'
        }
        response = self.client.post(self.register_user, missing_required_fields_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_list_serializer(self):
        user = User.objects.create(
            **{
                "username": "testuserSV",
                "first_name": "TestSV",
                "last_name": "UserSV",
                "email": "test_sv@example.com",
                "position": "Ceo",
                "password": "SuperSecurePassword1234!",
                "phone": "+491104510045",
            }
        )
        serializer = UserListSerializer(instance=user)
        self.assertEqual(serializer.data['first_name'], 'TestSV')
        self.assertEqual(serializer.data['last_name'], 'UserSV')
        self.assertEqual(serializer.data['email'], 'test_sv@example.com')
        self.assertEqual(serializer.data['position'], 'Ceo')
        self.assertEqual(serializer.data['phone'], '+491104510045')
        self.assertEqual(serializer.data['last_login'], None)

    def test_register_user_serializer(self):
        valid_payload = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'position': 'CEO',
            'password': 'SuperSecurePassword1234!',
            're_password': 'SuperSecurePassword1234!'
        }
        serializer = RegisterUserSerializer(data=valid_payload)
        self.assertTrue(serializer.is_valid())

    def test_register_user_serializer_invalid_data(self):
        invalid_payload = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'invalidemail',
            'position': 'Developer',
            'password': 'password123',
            're_password': 'password123'
        }
        serializer = RegisterUserSerializer(data=invalid_payload)
        self.assertFalse(serializer.is_valid())
