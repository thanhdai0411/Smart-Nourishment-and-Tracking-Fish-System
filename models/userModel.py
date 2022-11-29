import mongoengine as me
import bson


class User(me.Document):
    id = me.ObjectIdField(default=bson.ObjectId, primary_key=True)
    username = me.StringField()
    password = me.StringField()

    def to_json(self):
        return {"id": self.id,
                "username": self.username,
                "password": self.password}
