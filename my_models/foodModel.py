import mongoengine as me
import bson


class Food(me.Document):
    id = me.ObjectIdField(default=bson.ObjectId, primary_key=True)
    username = me.StringField()
    time = me.StringField()
    amount_food = me.StringField()
    status = me.StringField(default="WAITING")

    def to_json(self):
        return {"id": self.id,
                "time": self.time,
                "username": self.username,
                "amount_food": self.amount_food,
                "status": self.status
                }
