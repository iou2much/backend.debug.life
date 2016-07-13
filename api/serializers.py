#-*- coding: utf-8 -*-
from django.test import TestCase

# Create your tests here.
from django.forms import widgets
from rest_framework.compat import unicode_repr
from rest_framework import fields as drf_fields
from models import GoodsDocument

from rest_framework_mongoengine.serializers import (
    DocumentSerializer
)

class GoodsSerializer(DocumentSerializer):

    class Meta:
        model = GoodsDocument

    title = drf_fields.CharField(required=False, max_length=100)
    gid = drf_fields.IntegerField(required=False)
    count = drf_fields.CharField()
    band = drf_fields.CharField()
    url =  drf_fields.CharField()
    cat1 = drf_fields.CharField()
    cat2 = drf_fields.CharField()

    def restore_object(self, attrs, instance=None):
        if instance:
            instance.title = attrs.get('title', instance.title)
            instance.gid = attrs.get('gid', instance.gid)
            return instance

        # Create new instance
        return GoodsDocument(**attrs)
