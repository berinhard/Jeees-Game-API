from django.test import TestCase
from django.core.urlresolvers import reverse

__all__ = [
    'SingleTeamURLTests',
]

class SingleTeamURLTests(TestCase):

    def test_post_does_not_return_405(self):
        response = self.client.post(
            reverse('teams:single_team', kwargs={'team_uuid':'1234'})
        )
        self.assertNotEqual(response.status_code, 405)
