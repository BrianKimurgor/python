from mongoengine import Document, StringField, IntField, ListField

class Carpark(Document):
    name = StringField(required=True)
    location = StringField(required=True)
    totalSpaces = IntField(required=True, min_value=1)
    availableSpaces = IntField(required=True, min_value=1)
    ratePerHour = IntField(required=True, min_value=1)
    facilities = ListField(StringField(), default=[])

    meta = {
        'collection': 'carparks'
    }
