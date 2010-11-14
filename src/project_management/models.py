import uuid

from django.db import models
from django.db.models.signals import pre_save


class Project(models.Model):

    name = models.CharField(max_length=50)
    description = models.TextField()
    quality = models.IntegerField()
    initial_cash = models.IntegerField()
    uuid = models.CharField(max_length=36, blank=True)

def __set_project_uuid(sender, **kwargs):
    project = kwargs['instance']
    if not project.pk:
        project.uuid = str(uuid.uuid4())
pre_save.connect(__set_project_uuid, sender=Project)

class Release(models.Model):

    project = models.ForeignKey(Project)
    payment = models.IntegerField()
    position = models.IntegerField()
    #para simplificar deixaremos os componentes como atributos
    component_1 = models.IntegerField(null=True, blank=True)
    component_2 = models.IntegerField(null=True, blank=True)
    component_3 = models.IntegerField(null=True, blank=True)
    component_4 = models.IntegerField(null=True, blank=True)
