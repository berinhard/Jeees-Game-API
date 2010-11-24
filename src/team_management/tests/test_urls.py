from django.test import TestCase
from django.core.urlresolvers import reverse

__all__ = [
    'SingleTeamURLTests',
    'RootURLTests',
]

class SingleTeamURLTests(TestCase):

    def test_post_does_not_return_405(self):
        response = self.client.post(
            reverse('teams:single_team', kwargs={'team_uuid':'1234'})
        )
        self.assertNotEqual(response.status_code, 405)

    def test_get_does_not_return_405(self):
        response = self.client.get(
            reverse('teams:single_team', kwargs={'team_uuid':'1234'})
        )
        self.assertNotEqual(response.status_code, 405)


class RootURLTests(TestCase):

    def test_post_returns_405(self):
        response = self.client.post(reverse('teams:root'), {})
        self.assertEqual(response.status_code, 405)

    def test_get_does_not_return_405(self):
        response = self.client.get(reverse('teams:root'))
        self.assertNotEqual(response.status_code, 405)
