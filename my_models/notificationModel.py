import mongoengine as me
import bson


class Notification(me.Document):
    id = me.ObjectIdField(default=bson.ObjectId, primary_key=True)
    text = me.StringField()
    username = me.StringField()

    def to_json(self):
        return {"id": self.id,
                "username": self.username,
                "text": self.text,
                }
