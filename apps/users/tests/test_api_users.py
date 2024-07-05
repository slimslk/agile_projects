from django.test import TestCase

from rest_framework import status
from rest_framework.response import Response

from apps.projects.models import Project
from apps.users.choices.positions import Positions
from apps.users.models import User


class ApiUsersListTestCase(TestCase):
    fields_types = (
        ('first_name', str),
        ('last_name', str),
        ('email', str),
        ('position', str)
    )

    def setUp(self):
        users = [
            User(
                username='dimm_test_user',
                first_name='Dimm',
                last_name='Midd',
                email='dimm.midd@test.com',
                position=Positions.QA
            ),
            User(
                username='dimm_test_user_2',
                first_name='Lili',
                last_name='Bons',
                email='lili.bons@test.com',
                position=Positions.DESIGNER
            ),
        ]
        User.objects.bulk_create(users)

    def tearDown(self):
        User.objects.all().delete()

    def assertDictValuesTypes(self, dictionary, fields_n_types):
        for key, instance in fields_n_types:
            with self.subTest(key=key, value=dictionary[key], instance=instance):
                self.assertIsInstance(dictionary[key], instance)

    def test_get_all_users(self):
        response = self.client.get('/api/v1/users/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response, Response)

        self.assertIsInstance(response.data, list)

        for user in response.data:
            self.assertIsInstance(user, dict)
            self.assertDictValuesTypes(user, self.fields_types)


class ApiUsersEmptyListTestCase(TestCase):
    def test_empty_list(self):
        response = self.client.get('/api/v1/users/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 0)


class ApiUserCreateTestCase(TestCase):

    def test_create_valid_user(self):
        data = {
            "username": "dimm_test_user_retrieve",
            "first_name": "Dimm",
            "last_name": "Midd",
            "email": "dimm.midd@test.com",
            "position": "CEO",
            "password": "GreatPassword123",
            "re_password": "GreatPassword123",
        }

        response = self.client.post('/api/v1/users/register/', data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsInstance(response.data, dict)

        self.assertEqual(User.objects.get(username=data['username']).username, data['username'])
        self.assertEqual(User.objects.get(username=data['username']).first_name, data['first_name'])
        self.assertEqual(User.objects.get(username=data['username']).last_name, data['last_name'])
        self.assertEqual(User.objects.get(username=data['username']).email, data['email'])
        self.assertEqual(User.objects.get(username=data['username']).position, data['position'])

    def test_create_user_empty_data(self):
        data = {}
        response = self.client.post('/api/v1/users/register/', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsInstance(response.data, dict)


class ApiUserRetrieveTestCase(TestCase):
    fields_types = (
        ('username', str),
        ('first_name', str),
        ('last_name', str),
        ('email', str),
        ('position', str),
        ('phone', str),
        ('project', int),
    )

    def assertDictValuesTypes(self, dictionary, fields_n_types):
        for key, instance in fields_n_types:
            with self.subTest(key=key, value=dictionary[key], instance=instance):
                self.assertIsInstance(dictionary[key], instance)

    def setUp(self):
        proj = Project.objects.create(
            id=1,
            name="SAPHYR INC",
            description="Some kind of description"
        )
        self.user_data = {
            "id": 1,
            "username": 'dimm_test_user_retrieve',
            "first_name": 'Retrieve',
            "last_name": 'Checking',
            "email": 'dimm.midd@test.com',
            "phone": '+490001118877',
            "position": "CEO",
            "project": proj
        }
        User.objects.create(**self.user_data)

    def tearDown(self):
        Project.objects.all().delete()
        User.objects.all().delete()

    def test_retrieve_user_by_id(self):
        response = self.client.get('/api/v1/users/1/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response, Response)
        self.assertIsInstance(response.data, dict)

        self.assertDictValuesTypes(response.data, self.fields_types)

        self.assertEqual(response.data['username'], self.user_data['username'])
        self.assertEqual(response.data['first_name'], self.user_data['first_name'])
        self.assertEqual(response.data['last_name'], self.user_data['last_name'])
        self.assertEqual(response.data['email'], self.user_data['email'])
        self.assertEqual(response.data['phone'], self.user_data['phone'])
        self.assertEqual(response.data['position'], self.user_data['position'])
        self.assertEqual(response.data['project'], self.user_data['project'].id)

    def test_retrieve_non_existing_user(self):
        response = self.client.get('/api/v1/users/999/')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIsInstance(response, Response)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(str(response.data['detail']), 'No User matches the given query.')