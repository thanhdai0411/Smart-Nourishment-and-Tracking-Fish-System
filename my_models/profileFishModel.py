import mongoengine as me
import bson


class ProfileFish(me.Document):
    id = me.ObjectIdField(default=bson.ObjectId, primary_key=True)
    username = me.StringField()
    user_system = me.StringField()
    fish_type = me.StringField()
    time_start_farming = me.StringField()
    fish_name = me.StringField()
    note = me.StringField(default="Không có ghi chú về cư dân này")
    avatar = me.StringField()
    

    def to_json(self):
        return {"id": self.id,
                "user_system": self.user_system,
                "username": self.username,
                "fish_type": self.fish_type,
                "time_start_farming": self.time_start_farming,
                "fish_name": self.fish_name,
                "note": self.note,
                "avatar": self.avatar,
                }
