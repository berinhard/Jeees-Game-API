from django.test import TestCase

from project_management.models import Project

class TestProjectModel(TestCase):

    def setUp(self):
        self.params = {
            'name':'projeto',
            'description':'site web',
            'quality':10,
            'initial_cash':100,
        }

    def test_creates_project_uuid(self):
        project = Project(**self.params)
        self.assertFalse(project.uuid)
        project.save()
        self.assertTrue(project.uuid)

    def test_creates_project_uuid_on_creation(self):
        project = Project.objects.create(**self.params)
        self.assertTrue(project.uuid)

    def test_doesnt_change_uuid_value_on_update(self):
        project = Project.objects.create(**self.params)
        uuid = project.uuid
        project.name = 'new name'
        project.save()
        self.assertEqual(project.uuid, uuid)
