import uuid

from django.db import models
from django.db.models.signals import pre_save


class Project(models.Model):

    name = models.CharField(max_length=50)
    uuid = models.CharField(max_length=36)

def __set_project_uuid(sender, **kwargs):
    project = kwargs['instance']
    if not project.pk:
        project.uuid = str(uuid.uuid4())
pre_save.connect(__set_project_uuid, sender=Project)
