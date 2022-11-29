from email.policy import default
import mongoengine as me
import bson


class LabelFish(me.Document):
    id = me.ObjectIdField(default=bson.ObjectId, primary_key=True)
    name = me.StringField()
    user_id = me.ObjectIdField()

    def to_json(self):
        return {"id": self.id,
                "name": self.name,
                "user_id": self.user_id}
