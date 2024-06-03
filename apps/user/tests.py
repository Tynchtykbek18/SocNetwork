from rest_framework import status
from rest_framework.test import APITestCase


class UserTest(APITestCase):
    def test_user_registration(self):
        data = {
            "username_or_email": "admin",  # Может быть имя пользователя или электронная почта
            "password": "admin",
        }
        response = self.client.post("/api/v1/token/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("access" in response.data)
        self.assertTrue("refresh" in response.data)
        return response.data
