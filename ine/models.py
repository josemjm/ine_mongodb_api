from django.db import models
from jsonfield import JSONField

import uuid

# Create your models here.
class dict_ccaa(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    CODAUTO = models.CharField(max_length=2)
    NOMBRE = models.CharField(max_length=50)


class dict_provinces(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    CPRO = models.CharField(max_length=2)
    NOMBRE = models.CharField(max_length=50)


class dict_municipalities(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    CODAUTO = models.CharField(max_length=2)
    CPRO = models.CharField(max_length=2)
    CMUN = models.CharField(max_length=3)
    DC = models.CharField(max_length=1)
    NOMBRE = models.CharField(max_length=50)


class metadata(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=2)
    collections = JSONField()
    description = models.CharField(max_length=999)
    current_data = models.CharField(max_length=10)
    published_data = models.CharField(max_length=10)
