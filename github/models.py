#from __future__ import unicode_literals

#from django.db import models

from mongoengine import Document, DynamicDocument, EmbeddedDocument, fields

class User(Document):
    meta = {
        'collection': 'dl_users'
    }
    username = fields.StringField()
    password = fields.StringField()
    email = fields.StringField()
    first_name = fields.StringField(max_length=50)
    last_name = fields.StringField(max_length=50)

