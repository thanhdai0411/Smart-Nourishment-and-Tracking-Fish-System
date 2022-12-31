import mongoengine as me
import bson
import datetime


class LabelFish(me.Document):
    id = me.ObjectIdField(default=bson.ObjectId, primary_key=True)
    name = me.StringField()
    username = me.StringField()
    user_id = me.ObjectIdField()
    created_at = me.DateTimeField(default=datetime.datetime.utcnow)

    def to_json(self):
        return {"id": self.id,
                "name": self.name,
                "username": self.username,
                "user_id": self.user_id,
                "created_at": self.created_at
                }
