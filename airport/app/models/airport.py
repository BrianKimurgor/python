from mongoengine import Document, StringField, IntField, ListField

class Airport(Document):
    """
    A class to represent an Airport.

    Attributes
    ----------
    name : StringField
        The name of the airport. This field is required.
    location : StringField
        The location of the airport. This field is required.
    code : StringField
        The unique code of the airport. This field is required and must be unique.
    gates : IntField
        The number of gates in the airport. This field is required and must be at least 1.
    terminals : IntField
        The number of terminals in the airport. This field is required and must be at least 1.
    facilities : ListField
        A list of facilities available at the airport. Defaults to an empty list.

    Meta
    ----
    collection : str
        The name of the collection in the database where airport documents are stored.
    """
    name = StringField(required=True)
    location = StringField(required=True)
    code = StringField(required=True, unique=True)
    gates = IntField(required=True, min_value=1)
    terminals = IntField(required=True, min_value=1)
    facilities = ListField(StringField(), default=[])

    meta = {
        'collection': 'airports'
    }
