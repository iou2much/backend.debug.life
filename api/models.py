#-*- coding: utf-8 -*-
#from django.db import models
from mongoengine import Document, DynamicDocument, EmbeddedDocument, fields

class GoodsDocument(Document):
    meta = {
        'collection': 'kaola_goods'
    }

    gid = fields.IntField()
    title = fields.StringField()
    count = fields.IntField()
    band = fields.StringField()
    url = fields.StringField()
    cat1 = fields.StringField()
    cat2 = fields.StringField()

