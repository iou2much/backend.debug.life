#-*- coding: utf-8 -*-
#from django.db import models
from mongoengine import Document, DynamicDocument, EmbeddedDocument, fields

class ContainerDocument(Document):
    #meta = {
    #    'collection': 'kaola_goods'
    #}

    hostname = fields.StringField()
    user = fields.StringField()
    pwd = fields.StringField()
    #band = fields.StringField()
    #url = fields.StringField()
    #cat1 = fields.StringField()
    #cat2 = fields.StringField()

