import mongoengine as me
import bson


class ProfileFish(me.Document):
    id = me.ObjectIdField(default=bson.ObjectId, primary_key=True)
    username = me.StringField()
    fish_type = me.StringField()
    time_start_farming = me.StringField()
    fish_name = me.StringField()
    note = me.StringField()
    

    def to_json(self):
        return {"id": self.id,
                "username": self.username,
                "fish_type": self.fish_type,
                "time_start_farming": self.time_start_farming,
                "fish_name": self.fish_name
                "note": self.note
                }
