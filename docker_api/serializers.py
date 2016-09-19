#-*- coding: utf-8 -*-
from django.test import TestCase

# Create your tests here.
from django.forms import widgets
from rest_framework.compat import unicode_repr
from rest_framework import fields as drf_fields
from models import ContainerDocument

from rest_framework_mongoengine.serializers import (
    DocumentSerializer
)

class ContainerSerializer(DocumentSerializer):

    class Meta:
        model = ContainerDocument

    hostname = drf_fields.CharField(required=False, max_length=100)
    user = drf_fields.CharField(required=False)
    pwd = drf_fields.CharField(required=False)

    def restore_object(self, attrs, instance=None):
        if instance:
            instance.hostname = attrs.get('hostname', instance.hostname)
            instance.user = attrs.get('user', instance.user)
            instance.pwd  = attrs.get('pwd', instance.pwd)
            return instance

        # Create new instance
        return ContainerDocument(**attrs)
