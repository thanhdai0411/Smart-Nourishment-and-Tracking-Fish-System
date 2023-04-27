import mongoengine as me
import bson


class CountFish(me.Document):
    id = me.ObjectIdField(default=bson.ObjectId, primary_key=True)
    time_start = me.StringField()
    amount_eat = me.StringField()
    fish_count = me.ListField()
    eating_state = me.StringField()
    def to_json(self):
        return {"id": self.id,
                "time_start": self.time_start,
                "fish_count": self.fish_count,
                "amount_eat": self.amount_eat,
                "eating_state": self.eating_state,
                }
