from mongoengine import Document, StringField, IntField, ListField

class Airport(Document):
    name = StringField(required=True)
    location = StringField(required=True)
    code = StringField(required=True, unique=True)
    gates = IntField(required=True, min_value=1)
    terminals = IntField(required=True, min_value=1)
    facilities = ListField(StringField(), default=[])

    meta = {
        'collection': 'airports'
    }
