from django.test import TestCase
from django.core.urlresolvers import reverse


class GetProjectURLTests(TestCase):

    def test_post_returns_405(self):
        response = self.client.post(reverse(
            'projects:get_project', kwargs={'game_uuid':'123'}
        ), {})
        self.assertEqual(response.status_code, 405)

    def test_get_does_not_return_405(self):
        response = self.client.get(reverse(
            'projects:get_project', kwargs={'game_uuid':'123'}
        ))
        self.assertNotEqual(response.status_code, 405)

    def test_delete_returns_405(self):
        response = self.client.post(reverse(
            'projects:get_project', kwargs={'game_uuid':'123'}
        ))
        self.assertEquals(response.status_code, 405)
