import mongoengine as me
import bson


class StateDevice(me.Document):
    id = me.ObjectIdField(default=bson.ObjectId, primary_key=True)
    device = me.StringField()
    state = me.StringField()
    def to_json(self):
        return {"id": self.id,
                "device": self.device,
                "state": self.state,
                }
