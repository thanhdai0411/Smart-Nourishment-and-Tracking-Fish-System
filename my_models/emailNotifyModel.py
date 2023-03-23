import mongoengine as me
import bson


class EmailNotify(me.Document):
    id = me.ObjectIdField(default=bson.ObjectId, primary_key=True)
    username = me.StringField()
    email = me.StringField()
    

    def to_json(self):
        return {"id": self.id,
                "username": self.username,
                "user_id": self.user_id,
                "email": self.email,
                }
