from django.test import TestCase
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse

from game_config.decorators import user_auth
from utils.test_helpers import build_http_auth_header

class TestUserAuthDecorator(TestCase):

    def setUp(self):
        self.username = 'username'
        self.password = 'password'
        User.objects.create_user(
            username=self.username,
            email='a@a.com',
            password=self.password
        )

    def test_auth_with_correct_credentials(self):
        http_auth = build_http_auth_header(self.username, self.password)
        request = HttpRequest()
        request.META['HTTP_AUTHORIZATION'] = http_auth

        @user_auth
        def some_view(request):
            return HttpResponse('OK')

        response = some_view(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(request.user)

    def test_return_unauthorized_with_wrong_credentials(self):
        http_auth = build_http_auth_header(self.username, 'wrong')
        request = HttpRequest()
        request.META['HTTP_AUTHORIZATION'] = http_auth

        @user_auth
        def some_view(request):
            return HttpResponse('OK')

        response = some_view(request)
        self.assertEqual(response.status_code, 401)
